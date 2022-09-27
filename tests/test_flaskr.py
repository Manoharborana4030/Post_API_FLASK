import os
import tempfile
import response_server as run
import pytest
from flask import Flask


@pytest.fixture
def client():
    db_fd, run.app.config['DATABASE'] = tempfile.mkstemp()
    run.app.config['TESTING'] = True

    with run.app.test_client() as client:
        with run.app.app_context():
            run.init_db()
        yield client

    os.close(db_fd)
    os.unlink(run.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data