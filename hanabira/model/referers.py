# -*- coding: utf-8 -*-
import sqlalchemy as sql
from sqlalchemy.orm import eagerload #, relation
from sqlalchemy.ext.declarative import synonym_for
from sqlalchemy.dialects.mysql.base import BIGINT
from hanabira.model import meta
#from datetime import datetime
#import hashlib, random, string, time
#from pylons.i18n import _, ungettext
import logging
log = logging.getLogger(__name__)


class Referer(meta.Declarative):
    __tablename__ = "referers"
    referer_id = sql.Column(sql.Integer, primary_key=True)
    domain = sql.Column(sql.Unicode(64), nullable=False, index=True)
    date = sql.Column(sql.DateTime)
    referer = sql.Column(sql.UnicodeText)
    target = sql.Column(sql.UnicodeText)
    ip = sql.Column(sql.BIGINT, sql.ForeignKey('ips.ip'), nullable=True, index=True)
    session_id = sql.Column(sql.String(64), nullable=False)
    session_new = sql.Column(sql.Boolean, default=False)

    @synonym_for('referer_id')
    @property
    def id(self):
        return self.referer_id

    def commit(self):
        meta.Session.add(self)
        meta.Session.commit()
