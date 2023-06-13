from doit.tools import create_folder
from doit.task import clean_targets
import glob
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}



def task_extract_tr():
    """Extract translations from moodserver."""
    return {
            'actions': ['pybabel extract -o vksearch/bot/bot.pot vksearch/bot/__main__.py'],
            'targets': ['vksearch/bot/bot.pot'],
            'clean': [clean_targets],
           }


def task_update_tr():
    """Update translations."""
    return {
            'actions': ['pybabel update -D bot -i vksearch/bot/bot.pot -d vksearch/bot/po -l ru'],
            'file_dep': ['vksearch/bot/bot.pot'],
            'targets': ['vksearch/bot/po/ru/LC_MESSAGES/bot.po'],
           }


def task_compile_tr():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['vksearch/bot/po/ru/LC_MESSAGES']),
                'pybabel compile -D bot -d vksearch/bot/po -l ru'
                       ],
            'file_dep': ['vksearch/bot/po/ru/LC_MESSAGES/bot.po'],
            'targets': ['vksearch/bot/po/ru/LC_MESSAGES/bot.mo'],
            'clean': [clean_targets],
           }


def task_i18n():
    """Full translation."""
    return {
            'actions': [],
            'task_dep': ['extract_tr', 'update_tr', 'compile_tr'],
           }


def task_html():
    """Make HTML documentation."""
    return {
            'actions': ['sphinx-build -M html docs docs/_build'],
            'file_dep': glob.glob('*.rst') + ['vksearch/bot/__main__.py', 'vksearch/bot/limited_client.py', 'vksearch/bot/vk_filters.py', 'vksearch/bot/vk_requests.py'],
            'task_dep': ['i18n'],
            'targets': ['docs/_build'],
            'clean': [(shutil.rmtree, ['docs/_build']),],
           }


def task_test():
    """Test moodserver."""
    return {
            'actions': ['pytest'],
            'file_dep': ['test_vk.py', 'vksearch/bot/vk_requests.py', 'vksearch/bot/vk_filters.py'],
            'task_dep': ['i18n'],
            'verbosity': 2,
           }


def task_whl():
    """Build server wheel"""
    return {
            'actions': ['python3 -m build -nw vksearch'],
            'task_dep': ['i18n'],
            'file_dep': ['vksearch/bot/__main__.py', 'vksearch/bot/limited_client.py', 'vksearch/bot/vk_filters.py', 'vksearch/bot/vk_requests.py', 'vksearch/pyproject.toml', 'vksearch/bot/po/ru/LC_MESSAGES/bot.mo'],
            'targets': ['vksearch/dist/*.whl'],
            'clean': [(shutil.rmtree, ['vksearch/dist']), (shutil.rmtree, ['vksearch/build']), (shutil.rmtree, ['vksearch/MoodServer.egg-info'])],
           }

