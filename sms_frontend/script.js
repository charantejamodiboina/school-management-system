const API_URL = "http://127.0.0.1:8000/";

// Fetch data from the API
async function fetchData(endpoint) {
    try {
        const response = await fetch(API_URL + endpoint);
        if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error('Fetch operation failed:', error);
        return [];
    }
}

// Send data to the API
async function sendData(url, data) {
    try {
        const response = await fetch(API_URL + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error('Send operation failed:', error);
    }
}

// Load classes into the dropdown and class list
async function loadClasses() {
    try {
        const classes = await fetchData('api/class/');
        // Select dropdowns by their IDs
        const studentClassroomDropdown = document.getElementById('student-classroom');
        const subjectClassroomDropdown = document.getElementById('subject-classroom');

        // Clear existing options in both dropdowns
        studentClassroomDropdown.innerHTML = '<option value="" disabled selected>Select Classroom</option>'; // Reset dropdown
        subjectClassroomDropdown.innerHTML = '<option value="" disabled selected>Select Classroom</option>'; // Reset dropdown

        // Populate the options for each dropdown
        classes.forEach(classroom => {
            const option = document.createElement('option');
            option.value = classroom.id; // Set the ID of the classroom
            option.textContent = classroom.name; // Set the name of the classroom

            // Append the option to both dropdowns
            studentClassroomDropdown.appendChild(option.cloneNode(true)); // Append to the student dropdown
            subjectClassroomDropdown.appendChild(option.cloneNode(true)); // Append to the subject dropdown
        });

        const classList = document.getElementById('class-list');
        classList.innerHTML = classes.map(classroom => `<li>${classroom.name} - ${classroom.total_students}</li>`).join('');
    } catch (error) {
        console.error('Error fetching classrooms:', error);
    }
}

// Load classes into the dropdown and class list
async function loadTeachers() {
    try {
        const teachers = await fetchData('api/teachers/');
        const teachersDropdown = document.getElementById('subject-Teacher');
        teachersDropdown.innerHTML = '<option value="" disabled selected>Select Teacher</option>';
        
        teachers.forEach(teacher => {
            const option = document.createElement('option');
            option.value = teacher.id; // ID of the Teacher
            option.textContent = teacher.first_name; // Displayed name
            teachersDropdown.appendChild(option);
        });

        const teacherList = document.getElementById('teachers-list');
        teacherList.innerHTML = teachers.map(teacher => `<li>${teacher.first_name} - ${teacher.last_name} - ${teacher.email}</li>`).join('');
    } catch (error) {
        console.error('Error fetching teachers:', error);
    }
}

// Load students
async function loadStudents() {
    try {
        const students = await fetchData('api/students/');
        const studentsList = document.getElementById('students-list');
        studentsList.innerHTML = students.map(student => `<li>${student.first_name} ${student.last_name} - ${student.email}</li>`).join('');
    } catch (error) {
        console.error('Error fetching students:', error);
    }
}

// Load subjects
async function loadSubjects() {
    try {
        const subjects = await fetchData('api/subjects/');
        const subjectList = document.getElementById('subject-list');
        subjectList.innerHTML = subjects.map(subject => `<li>${subject.subject_name}</li>`).join('');
    } catch (error) {
        console.error('Error fetching subjects:', error);
    }
}
// Ensure the DOM is fully loaded before accessing elements
document.addEventListener('DOMContentLoaded', function () {
    const studentForm = document.getElementById('student-form');
    const classForm = document.getElementById('class-form');
    const teacherForm = document.getElementById('teacher-form');
    const subjectForm = document.getElementById('subject-form');

    // Add new student
    if (studentForm) {
        studentForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = {
                first_name: document.getElementById('student-first_name').value,
                last_name: document.getElementById('student-last_name').value,
                email: document.getElementById('student-email').value,
                phone_number: document.getElementById('student-phone_number').value,
                address: document.getElementById('student-address').value,
                date_of_birth: document.getElementById('student-date_of_birth').value,
                classroom: document.getElementById('student-classroom').value,
            };
            console.log("Submitting student:", data);
            await sendData('api/students/', data);
            studentForm.reset();
            loadStudents(); // Reload students after adding
        });
    }

        // Add new teacher
    if (teacherForm) {
        teacherForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = {
                first_name: document.getElementById('teacher-first_name').value,
                last_name: document.getElementById('teacher-last_name').value,
                email: document.getElementById('teacher-email').value,
                phone_number: document.getElementById('teacher-phone_number').value,
                hire_date: document.getElementById('teacher-hire_date').value,
            };
            console.log("Submitting teacher:", data);
            await sendData('api/teachers/', data);
            teacherForm.reset();
            loadTeachers(); // Reload teachers after adding
        });
    }

    // Add new subject
    if (subjectForm) {
        subjectForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = {
                subject_name: document.getElementById('subject-subject_name').value,
                Teacher: document.getElementById('subject-Teacher').value,
                classroom: document.getElementById('subject-classroom').value,
            };
            console.log("Submitting subject:", data);
            await sendData('api/subjects/', data);
            subjectForm.reset();
            loadSubjects(); // Reload students after adding
        });
    }


    // Add new class
    if (classForm) {
        classForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = {
                name: document.getElementById('class-name').value,
                total_students: parseInt(document.getElementById('class-total_students').value) || 0,
            };
            console.log("Submitting class:", data);
            const result=await sendData('api/class/', data);
            if (result) {
                console.log("Class added successfully:", result); // Success log
            } else {
                console.error("Failed to add class."); // Error log
            }
            classForm.reset();
            loadClasses(); // Reload classes after adding
        });
    }

    loadClasses(); // Initial load of classes
    loadStudents(); // Initial load of students
    loadTeachers();
    loadSubjects();
});
