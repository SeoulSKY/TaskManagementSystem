const toast = new Notyf();

/**
 * Create a new task input group
 * @returns {HTMLElement} The new input group
 */
function createTaskInput() {
  const newTaskInput = document.querySelector("#taskInput").cloneNode(true);
  newTaskInput.id = "";

  return newTaskInput;
}

/**
 * Create a new task card
 * @param {Task} task The task data to fill in
 * @returns {HTMLElement} The new task card
 */
function createTaskCard(task) {
  const newTaskCard = document.querySelector("#taskCard").cloneNode(true);
  newTaskCard.id = "";

  newTaskCard.querySelector("#taskCardTitle").textContent = task.title;
  newTaskCard.querySelector("#taskCardDescription").textContent =
    task.description;
  newTaskCard.querySelector("#taskCardPriority").textContent = task.priority;

  return newTaskCard;
}

/**
 * Remove all children of the given element
 *
 * @param {HTMLElement} element The element to remove children from
 */
function removeChildren(element) {
  [...element.children].forEach((child) => child.remove());
}

/**
 * Get the selected option from the given select element
 *
 * @param {HTMLElement} selectElement The select element containing the option
 * @return {HTMLElement | undefined} The selected option
 */
function getSelectedOption(selectElement) {
  return selectElement.options[selectElement.selectedIndex];
}

/**
 * Parse the elements in the given container to Task objects
 * @param {HTMLElement} container The container element containing task inputs
 * @returns {Promise<Task[]>} The parsed tasks from the given container element
 */
async function parseTasks(container) {
  return [...container.children].map((inputGroup) => {
    const title = inputGroup.querySelector("#createTitleInput").value;
    if (!title) {
      throw new Error("Title is required");
    }

    const description = inputGroup.querySelector(
      "#createDescriptionInput"
    ).value;

    if (!description) {
      throw new Error("Description is required");
    }

    const priority = getSelectedOption(
      inputGroup.querySelector("#createPrioritySelect")
    ).value;

    return { title, description, priority };
  });
}
