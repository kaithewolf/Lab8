<script>
    export let name;

    // Base vars
    const baseURL = "http://127.0.0.1:8192";

    // User vars
    let username = null;
	let password = null;
    let auth_token = null;

	// Global State
	let course_id = null;
	let student_id = null;
	let updated_grade = null;
	let sql_statement = null;

	// Fetched State
	let student_courses = [];
	let available_courses = [];
	let student_info = [];
	let teaching_courses = [];
	let edit_grade_output = null;
	let sql_output = null;

    // [DEBUG] Testing Things
    // username = "benjamindover";
	username = "jeffbezos"
	// username = "jman"
	password = "hunter2";
	course_id = "cse-999";
	student_id = "benjamindover";
	updated_grade = 60.8;
	sql_statement = 'SELECT * FROM users;';
    // auth_token = "FOE41n7e2fXOLLWGdMUkPlK9PpweLAxo8qTMj1Ds_RA";
	auth_token = "9hvj5-K-zxHdSc0utLglx6hZB7unuAb2j_k93l8M7RA"
	// auth_token = "brJrvWqBAn5XPU4nfdDGCeQLb3h5fl4oAq-Y9E88wc8"

    async function testLogin() {
        await login(username, password);
    }

    async function testLogout() {
        await logout(username, auth_token);
    }

    async function testGetEnrolled() {
        await get_enrolled_courses(username, auth_token);
    }

    async function testGetAll() {
        await get_all_courses(username, auth_token)
    }

    async function testRegister() {
        await register_for_course(username, auth_token, course_id);
    }

    async function testGetStudents() {
		await get_course_students(username, auth_token, course_id);
    }

    async function testGetTeaching() {
        await get_teaching_courses(username, auth_token);
    }

    async function testEditGrade() {
        await edit_grade(username, auth_token, course_id, student_id, updated_grade);
    }

    async function testRunSQL() {
		await execute_sql(username, auth_token, sql_statement);
    }

    // Shared Network Routines
    async function login(username, password) {
        // Create the request body
        const body = {"username": username, "password": password};

        // Make the request
        fetch(baseURL + "/api/v1/auth/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
            .then(response => {
                console.log(response);
                response.json().then(content => {
                    // Record the authentication token
                    auth_token = content.auth_token;
					console.log(auth_token)
                });
            })
            .catch(err => {
                console.error(err);
            });
    }

    async function logout(username, token) {
        // Create the request body
        const body = {"username": username, "token": token}

        // Make the request
        fetch(baseURL + "/api/v1/auth/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
            .then(response => {
                console.log(response);
                response.json().then(content => {
					// [TODO] Do something with response
                    console.log(content)
                });
            })
            .catch(err => {
                console.error(err);
            });
    }

    // Student Network Routines
    async function get_enrolled_courses(username, token) {
        // Create the request body
        const body = {"username": username, "token": token}

        // Make the request
        fetch(baseURL + "/api/v1/student/my_courses", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
			.then(response => {
				console.log(response);
				response.json().then(content => {
					console.log(content);
					student_courses = content;
				});
			})
            .catch(err => {
                console.error(err);
            });
    }

    async function get_all_courses(username, token) {
		// Create the request body
		const body = {"username": username, "token": token}

		// Make the request
		fetch(baseURL + "/api/v1/student/all_courses", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						console.log(content)
						available_courses = content;
					});
				})
				.catch(err => {
					console.error(err);
				});
    }

    async function register_for_course(username, token, course_id) {
		// Create the request body
		const body = {"username": username, "token": token, "course_id": course_id}

		// Make the request
		fetch(baseURL + "/api/v1/student/register_course", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						// [TODO] Do something with response
						console.log(content)
					});
				})
				.catch(err => {
					console.error(err);
				});
    }

    // Instructor Network Routines
    async function get_course_students(username, token, course_id) {
		// Create the request body
		const body = {"username": username, "token": token, "course_id": course_id}

		// Make the request
		fetch(baseURL + "/api/v1/instructor/course_students", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						console.log(content)
						student_info = content;
					});
				})
				.catch(err => {
					console.error(err);
				});
    }

    async function get_teaching_courses(username, token) {
		// Create the request body
		const body = {"username": username, "token": token}

		// Make the request
		fetch(baseURL + "/api/v1/instructor/my_courses", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						console.log(content)
						teaching_courses = content;
					});
				})
				.catch(err => {
					console.error(err);
				});
    }

    async function edit_grade(username, token, course_id, student_id, updated_grade) {
		// Create the request body
		const body = {
			"username": username,
			"token": token,
			"course_id": course_id,
			"student_id": student_id,
			"updated_grade": updated_grade
		}

		// Make the request
		fetch(baseURL + "/api/v1/instructor/edit_grade", {
			method: "PUT",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						console.log(content)
						edit_grade_output = content;
					});
				})
				.catch(err => {
					console.error(err);
				});
    }

    // Admin Network Routines
    async function execute_sql(username, token, sql_statement) {
		// Create the request body
		const body = {"username": username, "token": token, "sql_statement": sql_statement}

		// Make the request
		fetch(baseURL + "/api/v1/admin/sql_statement", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(body)
		})
				.then(response => {
					console.log(response);
					response.json().then(content => {
						console.log(content)
						sql_output = content;
					});
				})
				.catch(err => {
					console.error(err);
				});
    }
</script>

<main>
    <h3>Common</h3>

	<div>Username: <input bind:value={username} /></div>
	<div>Password: <input bind:value={password} /></div>
    <button on:click={testLogin}>Log In</button>
    <button on:click={testLogout}>Log Out</button>

	<hr>
	<hr>
	<hr>

    <h3>Student</h3>

	<h5>My Enrolled Courses:</h5>
	<button on:click={testGetEnrolled}>Get Enrolled Courses</button>
	<div>
		<table style="margin: auto;">
			<tr>
				<th>Course Abbreviation</th>
				<th>Course Name</th>
				<th>Instructor</th>
				<th>Time</th>
				<th>Students Enrolled</th>
				<th>Capacity</th>
			</tr>
			{#each student_courses as entry, i}
				<tr>
					<td>{entry["course_abbreviation"].toString()}</td>
					<td>{entry["course_name"].toString()}</td>
					<td>{entry["instructor"].toString()}</td>
					<td>{entry["time"].toString()}</td>
					<td>{entry["students_enrolled"].toString()}</td>
					<td>{entry["capacity"].toString()}</td>
				</tr>
			{/each}
		</table>
	</div>

	<h5>All Available Courses:</h5>
	<button on:click={testGetAll}>Get All Courses</button>
	<div>
		<table style="margin: auto;">
			<tr>
				<th>Course Abbreviation</th>
				<th>Course Name</th>
				<th>Instructor</th>
				<th>Time</th>
				<th>Students Enrolled</th>
				<th>Capacity</th>
			</tr>
			{#each available_courses as entry, i}
				<tr>
					<td>{entry["course_abbreviation"].toString()}</td>
					<td>{entry["course_name"].toString()}</td>
					<td>{entry["instructor"].toString()}</td>
					<td>{entry["time"].toString()}</td>
					<td>{entry["students_enrolled"].toString()}</td>
					<td>{entry["capacity"].toString()}</td>
				</tr>
			{/each}
		</table>
	</div>

	<h5>Register for Course:</h5>
	<div>Course Abbreviation: <input bind:value={course_id} /> <button on:click={testRegister}>Submit</button></div>



    <hr>
	<hr>
	<hr>

    <h3>Instructor</h3>

	<h5>Student Info for Course:</h5>
	<button on:click={testGetStudents}>Get Course Students</button>
	<div>Course Abbreviation: <input bind:value={course_id} /> <button on:click={testGetStudents}>Submit</button></div>
	<div>
		<table style="margin: auto;">
			<tr>
				<th>Name</th>
				<th>Grade</th>
			</tr>
			{#each student_info as entry, i}
				<tr>
					<td>{entry["name"].toString()}</td>
					<td>{entry["grade"].toString()}</td>
				</tr>
			{/each}
		</table>
	</div>

	<h5>Courses I'm Teaching:</h5>
	<button on:click={testGetTeaching}>Get Teaching Courses</button>
	<div>
		<table style="margin: auto;">
			<tr>
				<th>Course Abbreviation</th>
				<th>Course Name</th>
				<th>Time</th>
				<th>Students Enrolled</th>
				<th>Capacity</th>
			</tr>
			{#each teaching_courses as entry, i}
				<tr>
					<td>{entry["course_abbreviation"].toString()}</td>
					<td>{entry["course_name"].toString()}</td>
					<td>{entry["time"].toString()}</td>
					<td>{entry["students_enrolled"].toString()}</td>
					<td>{entry["capacity"].toString()}</td>
				</tr>
			{/each}
		</table>
	</div>

	<h5>Edit a Grade:</h5>
	<div>Course Abbreviation: <input bind:value={course_id} /></div>
	<div>Student ID: <input bind:value={student_id} /></div>
	<div>Updated Grade: <input bind:value={updated_grade} /></div>
	<button on:click={testEditGrade}>Submit Grade Change</button>


	<hr>
	<hr>
	<hr>

    <h3>Admin</h3>

	<div>SQL Statement: <input bind:value={sql_statement} /></div>
	<button on:click={testRunSQL}>Submit SQL to Server</button>
	<div>Results: {sql_output}</div>
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>