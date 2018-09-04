# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class DAO_Balance():

    __metaclass__=ABCMeta

    @abstractmethod
    def fill_dto_with_db(self):
        pass

    @abstractmethod
    def fill_db_with_dto(self):
        pass