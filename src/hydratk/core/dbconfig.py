# -*- coding: utf-8 -*-
"""HydraTK database configuration and settings module

.. module:: core.dbconfig
   :platform: Unix
   :synopsis: HydraTK database configuration and settings module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sqlite3 as cfgdb

"""
This structure contains all necessary commands for creating configuration database structure
"""
db_struct = {
    "table config" : """CREATE TABLE config(grp VARCHAR NOT NULL, obj VARCHAR NOT NULL, key VARCHAR NOT NULL, value VARCHAR, enabled INTEGER, 
                                 lvl4_key VARCHAR, lvl4_value VARCHAR, lvl5_key VARCHAR, lvl5_value VARCHAR)"""
}


class DBConfig():
    """ Class DBConfig
    """

    _db_file = None
    _conn = None

    def __init__(self, db_file):
        """Class constructor

           called when the object is initialized 

        Args:
           db_file (str): database file path           

        """

        self._db_file = db_file

    def connect(self):
        """Method connects configuration database

        Args:
           none

        Returns:
           void

        """

        self._conn = cfgdb.connect(self._db_file)

    def writedb(self, base_config):
        """Method writes configuration database using basic configuration

        Args:
           base_config (dict): configuration   

        Returns:
           bool: result 

        """

        result = False
        global db_struct
        with self._conn:
            cur = self._conn.cursor()
            for action, query in db_struct.items():
                cur.execute(query)
            cfg = self.cfg2db(base_config)
            cur.execute("begin")
            for item in cfg:
                if (item['value'].__class__.__name__ == 'list'):
                    for v in item['value']:
                        if (v != None):
                            cur.execute("insert into config (grp, obj, key, value, enabled, lvl4_key, lvl4_value) values(?,?,?,?,?,?,?)", (item[
                                        'grp'], item['obj'], item['key'], None, 1, None, v))
                elif (item['value'].__class__.__name__ == 'dict'):
                    for k, v in item['value'].items():
                        if (v.__class__.__name__ == 'list'):
                            for v2 in v:
                                if (v2 != None):
                                    cur.execute("insert into config (grp, obj, key, value, enabled, lvl4_key, lvl4_value, lvl5_key, lvl5_value) values(?,?,?,?,?,?,?,?,?)", (item[
                                                'grp'], item['obj'], item['key'], None, 1, k, None, None, v2))
                        elif (v.__class__.__name__ == 'dict'):
                            for k2, v2 in v.items():
                                if (v2 != None):
                                    cur.execute("insert into config (grp, obj, key, value, enabled, lvl4_key, lvl4_value, lvl5_key, lvl5_value) values(?,?,?,?,?,?,?,?,?)", (item[
                                                'grp'], item['obj'], item['key'], None, 1, k, None, k2, v2))
                        else:
                            if (v != None):
                                cur.execute("insert into config (grp, obj, key, value, enabled, lvl4_key, lvl4_value) values(?,?,?,?,?,?,?)", (item[
                                            'grp'], item['obj'], item['key'], None, 1, k, v))
                else:
                    cur.execute("insert into config (grp, obj, key, value, enabled) values(?,?,?,?,?)", (item[
                                'grp'], item['obj'], item['key'], item['value'], 1))
            self._conn.commit()
            result = True
        return result

    def cfg2db(self, d):
        """Method converts base config data to the database input format

        Args:
           d (dict): base configuration   

        Returns:
           dict: cfg 

        """

        cfg = []
        for gk, gv in d.items():
            for ok, ov in gv.items():
                for kk, kv in ov.items():
                    cfg.append({'grp': gk, 'obj': ok, 'key': kk, 'value': kv})
        return cfg

    def db2cfg(self, active_only=False):
        """Method converts config database data to base config input format

        Args:
           active_only (bool): whether to load only active settings, default False   

        Returns:
           list: records 

        """

        enabled_filter = "enabled = 1" if active_only == True else "1 = 1"
        with self._conn:
            cur = self._conn.cursor()
            cur.execute("select * from config where %s" % (enabled_filter))
            return cur.fetchall()
