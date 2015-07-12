from zp_library.models import Notice

def add_notice(content):
    Notice(contents=content).put()

def get_notice(limit=None):
    notice_query = Notice.query().order(-Notice.date)
    notice_result = notice_query.fetch(limit=limit)

    return notice_result
