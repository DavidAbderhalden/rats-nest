"""Handling incoming requests with invalid payload"""
from fastapi import Request

class AppExceptionHandler(Exception):
    def __init__(self):
        print('Implement')

    @staticmethod
    def handle_exception_case(request: Request):
        return request
