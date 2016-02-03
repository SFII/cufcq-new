from models.fcq import Fcq

def generate():
    fcq_cursor = Fcq().cursor()
    instructor_id = None
    course_id = None
    department_id = None
    for fcq_data in fcq_data_cursor:
        fcq_id = fcq_data['id']
        if fcq_data['department_id'] is None:
            department_id = generate_instructor(fcq_data)
        else:
            department_id = fcq_data['department_id']
        if fcq_data['instructor_id'] is None:
            instructor_id = generate_instructor(fcq_data, department_id)
        else:
            instructor_id = fcq_data['instructor_id']
        if fcq_data['course_id'] is None:
            course_id = generate_instructor(fcq_data, department_id)
        else:
            course_id = fcq_data['course_id']
        Course().append_item_to_listfield(course_id, 'instructors', instructor_id)
        Course().append_item_to_listfield(course_id, 'fcqs', fcq_id)
        Instructor().append_item_to_listfield(instructor_id, 'courses', course_id)
        Instructor().append_item_to_listfield(instructor_id, 'fcqs', fcq_id)
        Department().append_item_to_listfield(department_id, 'instructors', instructor_id)
        Department().append_item_to_listfield(department_id, 'courses', course_id)
        Department().append_item_to_listfield(department_id, 'fcqs', fcq_id)
        updated_ids = {
            'department_id': department_id,
            'course_id': course_id,
            'instructor_id': instructor_id
        }
        Fcq().update_item(fcq_id, updated_ids)

#First pass: Iterate through fcqs; create department, course, instructor. tie department_id to course and instructor
#Second pass:


def generate_instructor(fcq_data, department_id=None):
    sanitized = Instructor().sanitize_from_raw(fcq_data)
    sanitized['department_id'] = department_id
    slug = sanitized['slug']
    instructor_id = Instructor().create_item(sanitized)
    if instructor_id is None:
        instructor_id = Instructor().find_item({'slug': slug})[0]
    return instructor_id

def generate_course(fcq_data, department_id=None):
    sanitized = Course().sanitize_from_raw(fcq_data)
    sanitized['department_id'] = department_id
    slug = sanitized['slug']
    course_id = Course().create_item(sanitized)
    if course_id is None:
        course_id = Course().find_item({'slug': slug})[0]
    return course_id

def generate_department(fcq_data):
    sanitized = Department().sanitize_from_raw(fcq_data)
    slug = sanitized['slug']
    department_id = Department().create_item(sanitized)
    if department_id is None:
        department_id = Department().find_item({'slug': slug})[0]
    return department_id
