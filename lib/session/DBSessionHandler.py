#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        DBSessionHandler
# Purpose:     DBのセッションハンドラ
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import time
from time import gmtime
from SessionHandler import SessionHandler
from lib import DBAccess

class DBSessionHandler(SessionHandler):
    """
    DBセッションハンドラ
    """
    def __init__(self, setting):
        self.setting = setting
        self.dba = DBAccess.order()
    def create(self, session_id):
        """
        セッション生成
        """
        try:
            self.dba.insert('session_tbl', {'id':session_id, 'data':'', 'update_time':time.mktime(gmtime())})
            self.dba.commit()
            return True
        except:
            return False
    def read(self, session_id, lifetime):
        """
        セッション読み込み
        """
        if session_id is not None:
            res = self.dba.select('session_tbl', fields='data', where={'id':session_id, 'update_time>':time.mktime(gmtime())-lifetime})
            if len(res) == 1:
                return res[0]['data'].encode('utf-8')
        return None
    def write(self, session_id, data):
        """
        セッション書き込み
        """
        if session_id is not None:
            res = self.dba.update(table='session_tbl', sets={'data':data, 'update_time':time.mktime(gmtime())}, where={'id':session_id})
            if res == 0:
                self.dba.insert('session_tbl', {'id':session_id, 'data':data, 'update_time':time.mktime(gmtime())})
            self.dba.commit()

    def delete(self, session_id):
        """
        セッション削除
        """
        if session_id is not None:
            self.dba.delete('session_tbl', where={'id':session_id})
            self.dba.commit()
    def close(self):
        """
        セッション終了
        """
#        self.dba.close()
    def gc(self, lifetime):
        """
        ガーベジコレクション
        """
        self.dba.execute_sql('DELETE FROM session_tbl WHERE update_time+:lifetime > :now',{'lifetime':lifetime, 'now':time.mktime(gmtime())})
        self.dba.commit()

if __name__ == '__main__':
    import uuid
    setting={
        'sql':'sqlite',
        'host':'',
        'db':':memory:',
    }
    lifetime = 1440
    dba = DBAccess.create(setting)
    id = None
    for i in range(10):
        data = handler.read(id, lifetime)
        if data is None:
            data = ''
        print (data)
        handler.delete(id)
        if id is None:
            id = '%s'%uuid.uuid4()
        data += 'A'
        handler.write(id, data)

