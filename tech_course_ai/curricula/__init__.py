from curricula.git_masterclass import GIT_COURSE
from curricula.devops_cloud import DEVOPS_COURSE
from curricula.mobile_dev import MOBILE_COURSE

AVAILABLE_COURSES = {
    "git": GIT_COURSE,
    "git_masterclass": GIT_COURSE,
    "devops": DEVOPS_COURSE,
    "devops_cloud": DEVOPS_COURSE,
    "mobile": MOBILE_COURSE,
    "mobile_dev": MOBILE_COURSE
}

def get_course(course_id: str):
    """Retrieves course dictionary by ID or alias."""
    return AVAILABLE_COURSES.get(course_id.lower(), GIT_COURSE)
