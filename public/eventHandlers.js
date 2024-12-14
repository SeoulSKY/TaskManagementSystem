function onAddFieldClick() {
  document.querySelector("#createTaskContainer").appendChild(createTaskInput());
}

async function onCreateSubmit() {
  const container = document.querySelector("#createTaskContainer");

  let tasks;
  try {
    tasks = await parseTasks(container);

    if (tasks.length === 1) {
      await addTask(tasks[0]);
    } else {
      await addTasks(tasks);
    }
  } catch (err) {
    toast.error(err.message);
    console.error(err);
    return;
  }

  removeChildren(container);

  tasks.forEach((task) => {
    container.appendChild(createTaskCard(task));
  });

  toast.success("Task added successfully");

  onResetFieldsClick();
}

function onResetFieldsClick() {
  const container = document.querySelector("#createTaskContainer");
  removeChildren(container);
  container.appendChild(createTaskInput());
}

async function onReadTitleSubmit() {
  const titleInput = document.querySelector("#readTitleInput");
  const option = getSelectedOption(document.querySelector("#readTitleSelect"));

  if (!titleInput.value) {
    toast.error("Title is required");
    return;
  }

  let tasks;
  try {
    if (option.value === "match") {
      tasks = [await getTask(titleInput.value)];
    } else {
      tasks = await searchTitle(titleInput.value);
    }
  } catch (err) {
    toast.error(err.message);
    console.error(err);
    return;
  }

  const container = document.querySelector("#readTaskContainer");

  removeChildren(container);

  if (tasks.length === 0) {
    toast.error("No tasks found");
    return;
  }

  tasks.forEach((task) => {
    container.appendChild(createTaskCard(task));
  });

  titleInput.value = "";
}

async function onReadDescriptionSubmit() {
  const descriptionInput = document.querySelector("#readDescriptionInput");

  if (!descriptionInput.value) {
    toast.error("Keyword is required");
    return;
  }

  let tasks;
  try {
    tasks = await searchDescription(descriptionInput.value);
  } catch (err) {
    toast.error(err.message);
    console.error(err);
    return;
  }

  const container = document.querySelector("#readTaskContainer");

  removeChildren(container);

  if (tasks.length === 0) {
    toast.error("No tasks found");
    return;
  }

  tasks.forEach((task) => {
    container.appendChild(createTaskCard(task));
  });

  descriptionInput.value = "";
}

async function onReadPrioritySubmit() {
  const option = getSelectedOption(
    document.querySelector("#readPrioritySelect")
  );

  let tasks;
  try {
    if (option.value === "all") {
      tasks = await getAllTasks();
    } else {
      tasks = await searchPriority(option.value);
    }
  } catch (err) {
    toast.error(err.message);
    console.error(err);
    return;
  }

  const container = document.querySelector("#readTaskContainer");

  removeChildren(container);

  if (tasks.length === 0) {
    toast.error("No tasks found");
    return;
  }

  tasks.forEach((task) => {
    container.appendChild(createTaskCard(task));
  });
}

async function onUpdateEnter() {
  let tasks;
  try {
    tasks = await getAllTasks();
  } catch (err) {
    console.error(err);
    toast.error(err.message);
    return;
  }

  const container = document.querySelector("#updateTaskContainer");
  removeChildren(container);

  tasks.forEach((task) => {
    const taskInput = createTaskInput(task);
    const titleInput = taskInput.querySelector("#createTitleInput");
    titleInput.value = task.title;
    titleInput.disabled = true;

    taskInput.querySelector("#createDescriptionInput").value = task.description;

    [...taskInput.querySelector("#createPrioritySelect").options].find(
      (option) => option.value === task.priority
    ).selected = true;

    container.appendChild(taskInput);
  });
}

async function onUpdateSubmit() {
  try {
    for (const task of await parseTasks(
      document.querySelector("#updateTaskContainer")
    )) {
      await updateTask(task);
    }
  } catch (err) {
    console.error(err);
    toast.error(err.message);
    return;
  }

  toast.success("Tasks updated successfully");
}
