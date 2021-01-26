"""
CheckiOReferee is a base referee for checking you code.
    arguments:
        tests -- the dict contains tests in the specific structure.
            You can find an example in tests.py.
        cover_code -- is a wrapper for the user function and additional operations before give data
            in the user function. You can use some predefined codes from checkio.referee.cover_codes
        checker -- is replacement for the default checking of an user function result. If given, then
            instead simple "==" will be using the checker function which return tuple with result
            (false or true) and some additional info (some message).
            You can use some predefined codes from checkio.referee.checkers
        add_allowed_modules -- additional module which will be allowed for your task.
        add_close_builtins -- some closed builtin words, as example, if you want, you can close "eval"
        remove_allowed_modules -- close standard library modules, as example "math"
checkio.referee.checkers
    checkers.float_comparison -- Checking function fabric for check result with float numbers.
        Syntax: checkers.float_comparison(digits) -- where "digits" is a quantity of significant
            digits after coma.
checkio.referee.cover_codes
    cover_codes.unwrap_args -- Your "input" from test can be given as a list. if you want unwrap this
        before user function calling, then using this function. For example: if your test's input
        is [2, 2] and you use this cover_code, then user function will be called as checkio(2, 2)
    cover_codes.unwrap_kwargs -- the same as unwrap_kwargs, but unwrap dict.
"""

from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee
# from checkio.referees import cover_codes

from tests import TESTS

MOVES = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
ROLL = {
    'N': dict(zip('DUNSWE', 'SNDUWE')),
    'S': dict(zip('DUNSWE', 'NSUDWE')),
    'W': dict(zip('DUNSWE', 'EWNSDU')),
    'E': dict(zip('DUNSWE', 'WENSUD')),
}

"""
@kurosawa4434

js_anim is here to give data for your javascript visualization.
js_anim[n][0]: position (row, column) of the cube at step n.
js_anim[n][1]: list of positions of the colored cells at step n.
js_anim[n][2]: list of colored faces of the cube at step n.

Then it sends you: (message for user, number of rows, number of cols, js_anim)
Feel free to change it as you see fit!
"""


def checker(data, user_result):
    (nrows, ncols), pos, colored = data
    # Get right types from "test data".
    pos, colored = tuple(pos), set(map(tuple, colored))
    faces = set()

    js_anim = [[pos, sorted(colored), sorted(faces)]]

    try:
        assert isinstance(user_result, str), 'You must return a string.'
        assert user_result, 'You must return some directions to roll the cube.'
        forbidden_chars = ''.join(sorted(set(user_result) - set('NSWE')))
        assert not forbidden_chars, \
            'You must return NSWE directions, not %r.' % forbidden_chars

        for nsteps, move in enumerate(user_result, 1):
            (r, c), (dr, dc) = pos, MOVES[move]
            r, c = pos = r + dr, c + dc
            faces = set(map(ROLL[move].get, faces))
            catch_down = pos in colored and 'D' not in faces
            leave_down = pos not in colored and 'D' in faces
            if catch_down:
                faces.add('D')
                colored.remove(pos)
            is_solved = len(faces) == 6
            if leave_down:
                faces.remove('D')
                colored.add(pos)

            js_anim.append([pos, sorted(colored), sorted(faces)])

            assert 0 <= r < nrows and 0 <= c < ncols, \
                'Step %d: you are outside the grid at %s.' % (nsteps, pos)
            if is_solved:
                break

        else:
            message = 'After %d steps, there are %d face(s) still uncolored.'
            raise AssertionError(message % (nsteps, 6 - len(faces)))

        assert len(user_result) == nsteps, "It's colorful, stop rolling."

    except AssertionError as error:
        return False, [error.args[0], nrows, ncols, js_anim]

    else:
        win_message = 'You colored the cube in %d steps.' % nsteps
        return True, [win_message, nrows, ncols, js_anim]


cover_input = '''
def cover(func, in_data):
    dimensions, start, colored = in_data
    return func(tuple(dimensions), tuple(start), set(map(tuple, colored)))
'''


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        checker=checker,
        function_name={
            'python': 'roll_cube',
            # 'js': 'rollCube',
        },
        cover_code={
            'python-3': cover_input,
            # 'js-node': cover_codes.unwrap_args,
        },
    ).on_ready,
)
