import simplejson as json
import unittest
from datetime import datetime
from sqlalchemy import inspect
from flask import Flask, jsonify
from app import app,db,base
from sqlalchemy.orm import joinedload

class test(unittest.TestCase):
  boardPostColumns = [
    'updated_at',
    'board_elements',
    'title',
    'created_at',
    'id'
  ]

  boardGetAllColumns = [
    'inprogress_count',
    'todo_count',
    'title',
    'created_at',
    'updated_at',
    'id',
    'done_count'
  ]

  boardGetColumns = [
    'title',
    'created_at',
    'updated_at',
    'done',
    'inprogress',
    'todo',
    'id'
  ]

  elementPostColumns = [
    'board_id',
    'category',
    'description',
    'created_at',
    'updated_at',
    'id'
  ]

  def input_dict_to_args(self, input_dict):
    return '&'.join(['%s=%s' % tup for tup in input_dict.items()])

  def is_sub(self, sub, lst):
    lst_s = set(lst)
    for s in sub:
      if s not in lst_s:
        return False
    return True

  def object_as_dict(self, obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

  def commit(self):
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      print(e)

  def post(self, input_data, modelType):
    return self.app.post('/kanban/%s?%s' % (modelType, self.input_dict_to_args(input_data)), follow_redirects=False)

  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True
    self.app_context = app.app_context()
    self.app_context.push()

  def tearDown(self):
    db.session.execute('DELETE FROM elements;')
    self.commit()
    db.session.execute('DELETE FROM boards;')
    self.commit()
    self.app_context.pop()

  def test_create_board(self):
    input_data = dict(title='My Awesome Board')
    result = json.loads(self.post(input_data, 'boards').data)
    assert(self.is_sub(self.boardPostColumns,result['data']['board'].keys()))
    assert(not result['data']['board']['board_elements'])
    assert(result['success'])

  def test_delete_board(self):
    input_data = dict(title='My Awesome Board')
    result = json.loads(self.post(input_data, 'boards').data)
    result_id = int(result['data']['board']['id'])
    input_data = dict(id=result_id)
    result = json.loads(self.app.delete('/kanban/boards?%s' % self.input_dict_to_args(input_data), follow_redirects=False).data)
    assert(result == {'success': True})

    boards = json.loads(self.app.get('/kanban/boards').data)['data']['boards']
    has_board = len([b['id'] for b in boards if b['id'] == result_id]) > 0
    assert(not has_board)

  def test_create_element(self):
    input_data = dict(title='My Awesome Board')
    result = json.loads(self.post(input_data, 'boards').data)
    result_id1 = int(result['data']['board']['id'])
    input_data = dict(
      board_id=result_id1,
      description='A Todo Task, I should get this done!',
      category='todo'
    )
    result = json.loads(self.post(input_data, 'board_elements').data)
    element = result['data']['board_element']
    assert(self.is_sub(self.elementPostColumns, element.keys()))
    assert(element['board_id'] == input_data['board_id'])
    assert(element['description'] == input_data['description'])
    assert(element['category'] == input_data['category'])
    assert(result['success'])

  def test_delete_element(self):
    input_data = dict(
       title='My Awesome Board')
    result = json.loads(self.post(input_data, 'boards').data)
    result_id1 = int(result['data']['board']['id'])
    input_data = dict(
      board_id=result_id1,
      description='A Todo Task, I should get this done!',
      category='todo'
    )
    result = json.loads(self.post(input_data, 'board_elements').data)
    result_id = int(result['data']['board_element']['id'])
    input_data = dict(board_element_id = result_id)
    result = json.loads(
      self.app.delete(
      '/kanban/board_elements?%s' % self.input_dict_to_args(input_data),
      follow_redirects=False).data)
    assert(result == {'success': True})

  def test_get_boards(self):
    input_data1 = dict(
      title='My Awesome Board')
    input_data2 = dict(
      title='My Awesome Board 2')
    result_id1 = json.loads(self.post(input_data1, 'boards').data)['data']['board']['id']
    result_id2 = json.loads(self.post(input_data2, 'boards').data)['data']['board']['id']
    input_data1 = dict(
      board_id=result_id1,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data2 = dict(
      board_id=result_id1,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data3 = dict(
      board_id=result_id2,
      description='A Todo Task, I should get this done!',
      category='todo')
    input_data4 = dict(
      board_id=result_id2,
      description='A Todo Task, I should get this done!',
      category='done')
    self.post(input_data1, 'board_elements')
    self.post(input_data2, 'board_elements')
    self.post(input_data3, 'board_elements')
    self.post(input_data4, 'board_elements')
    result = json.loads(self.app.get('/kanban/boards').data)
    boards = result['data']['boards']
    assert(self.is_sub(self.boardGetAllColumns,boards[0].keys()))
    assert(result['success'])
    assert(result['data']['boards'][0]['todo_count']) == 0
    assert(result['data']['boards'][0]['inprogress_count']) == 2
    assert(result['data']['boards'][0]['done_count']) == 0
    assert(result['data']['boards'][1]['todo_count']) == 1
    assert(result['data']['boards'][1]['inprogress_count']) == 0
    assert(result['data']['boards'][1]['done_count']) == 1

  def test_get_board(self):
    input_data = dict(title='My Awesome Board')
    result_id = json.loads(self.post(input_data, 'boards').data)['data']['board']['id']
    input_data1 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data2 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data3 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='todo')
    input_data4 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='done')
    self.post(input_data1, 'board_elements')
    self.post(input_data2, 'board_elements')
    self.post(input_data3, 'board_elements')
    self.post(input_data4, 'board_elements')
    result = json.loads(self.app.get('/kanban/boards/%s' % result_id).data)
    board = result['data']['board']
    assert(len(board['todo']) ==  1)
    assert(len(board['inprogress']) ==  2)
    assert(len(board['done']) ==  1)
    assert(self.is_sub(self.boardGetColumns,board.keys()))
    assert(self.is_sub(self.elementPostColumns,board['todo'][0].keys()))
    assert(result['success'])

  def test_advance_element(self):
    input_data = dict(title='My Awesome Board')
    result_id = json.loads(self.post(input_data, 'boards').data)['data']['board']['id']
    input_data1 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data2 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='inprogress')
    input_data3 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='todo')
    input_data4 = dict(
      board_id=result_id,
      description='A Todo Task, I should get this done!',
      category='done')
    self.post(input_data1, 'board_elements')
    self.post(input_data2, 'board_elements')
    result_id2 = json.loads(self.post(input_data3, 'board_elements').data)['data']['board_element']['id']
    result_id3 = json.loads(self.post(input_data4, 'board_elements').data)['data']['board_element']['id']
    result = json.loads(self.app.get('/kanban/boards').data)
    assert(result['data']['boards'][0]['todo_count'] == 1)
    assert(result['data']['boards'][0]['inprogress_count'] == 2)
    assert(result['data']['boards'][0]['done_count'] == 1)
    input_data1 = dict(id=result_id2)
    result = json.loads(self.post(input_data1, 'board_elements/advance').data)
    assert(result == {'success': True})
    input_data2 = dict(id=result_id3)
    self.post(input_data2, 'board_elements/advance')
    result = json.loads(self.app.get('/kanban/boards').data)
    assert(result['data']['boards'][0]['todo_count'] == 0)
    assert(result['data']['boards'][0]['inprogress_count'] == 3)
    assert(result['data']['boards'][0]['done_count'] == 1)

if __name__ == '__main__':
  unittest.main()
