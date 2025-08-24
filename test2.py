from functools import cached_property



class TestClass:

    @cached_property
    def abc(self) -> str:
        return "abc"
    


tc = TestClass()
print(tc.__dict__["abc"])