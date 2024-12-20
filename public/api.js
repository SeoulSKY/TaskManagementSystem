/**
 * @typedef {("LOW"|"MEDIUM"|"HIGH")} Priority
 */

/**
 * @typedef {("HEAD"|"GET"|"POST"|"PUT"|"DELETE") RequestMethod
 */

/**
 * @typedef {Object} Task
 * @property {string} title
 * @property {string} description
 * @property {Priority} priority
 */

const BASE_URL = "http://localhost:8000/api/";

/**
 * Send an HTTP request to the specified server endpoint with the given method and data.
 * @private
 * @param {string} endpoint The endpoint to send the request to.
 * @param {Record<string, any>} data The data to send to the server.
 * @param {RequestMethod} method The request method.
 * @returns {Promise<undefined | Task | Task[]>} The response body of the request.
 */
async function request(endpoint, data = {}, method = "GET") {
  const url = new URL(BASE_URL + endpoint);
  const settings = { method };

  if (["HEAD", "GET", "DELETE"].includes(method)) {
    const params = new URLSearchParams(data);
    url.search = params.toString();
  } else {
    settings.headers = {
      "Content-Type": "application/json",
    };
    settings.body = JSON.stringify(data);
  }

  const response = await fetch(url, settings);

  let json;
  try {
    json = await response.json();
  } catch (err) {
    return undefined;
  }

  if (json && json.detail) {
    throw new Error(json.detail);
  }

  return json || undefined;
}

/**
 * Get a task that matches the given title.
 * @param {string} title The title of the task.
 * @returns {Promise<Task>} The task object.
 * @throws {Error} If the task does not exist.
 */
async function getTask(title) {
  return request("task", { title });
}

/**
 * Add a task to the list of tasks.
 * @param {Task} task The task object to add.
 * @throws {Error} If the task already exists in the list.
 */
async function addTask(task) {
  return request("task", task, "POST");
}

/**
 * Update a task in the list of tasks.
 * @param {Task} task The task object to update.
 * @returns {Promise<void>}
 * @throws {Error} if the task is not on the list of tasks.
 */
async function updateTask(task) {
  return request("task", task, "PUT");
}

/**
 * Delete a task that matches the given title.
 * @param {string} title The title of the task to delete.
 * @returns {Promise<void}
 * @throws {Error} If the task does not exist.
 */
async function deleteTask(title) {
  return request("task", { title }, "DELETE");
}

/**
 * Get all tasks sorted by their priority.
 * @returns {Promise<Task[]>} The tasks sorted by their priority.
 */
async function getAllTasks() {
  return request("tasks");
}

/**
 * Add tasks to the list of tasks.
 * @param {Task[]} tasks The tasks to add.
 * @returns {Promise<void>}
 * @throws {Error} If any of the tasks already exist in the list.
 */
async function addTasks(tasks) {
  return request("tasks", tasks, "POST");
}

/**
 * Clear tasks from the list of tasks.
 * @returns {Promise<void>}
 */
async function clearTasks() {
  return request("tasks", {}, "DELETE");
}

/**
 * Search all tasks that have the given keyword in their titles.
 * @param {string} keyword The keyword to search for.
 * @returns {Promise<Task[]>} The search results.
 */
async function searchTitle(keyword) {
  return request("search/title", { keyword });
}

/**
 * Search all tasks that have the given keyword in their descriptions.
 * @param {string} keyword The keyword to search for.
 * @returns {Promise<Task[]>} The search results.
 */
async function searchDescription(keyword) {
  return request("search/description", { keyword });
}

/**
 * Search all tasks that have the given priority.
 * @param {Priority} priority The priority to search for.
 * @returns {Promise<Task[]>} The search results.
 */
async function searchPriority(priority) {
  return request("search/priority", { priority });
}
