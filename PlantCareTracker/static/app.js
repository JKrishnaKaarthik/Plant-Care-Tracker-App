document.addEventListener("DOMContentLoaded", function () {
  const appElement = document.getElementById("app");

  const state = {
    newPlant: {
      name: "",
      species: "",
      careLevel: "",
      waterSchedule: "",
    },
    plants: [],
  };

  function render() {
    appElement.innerHTML = `
                  <div class="section">
                      <h2>Add a New Plant</h2>
                      <form id="plantForm" class="form" >
                          <label for="name">Name:</label>
                          <input type="text" id="name" value="${
                            state.newPlant.name
                          }" required>
                          <label for="species">Species:</label>
                          <input type="text" id="species" value="${
                            state.newPlant.species
                          }" required>
                          <label for="careLevel">Care Level:</label>
                          <input type="text" id="careLevel" value="${
                            state.newPlant.careLevel
                          }" required>
                          <label for="waterSchedule">Water Schedule:</label>
                          <input type="text" id="waterSchedule" value="${
                            state.newPlant.waterSchedule
                          }" required>
                          <button type="button" onclick="addPlant()">Add Plant</button>
                      </form>
                  </div>
                  <div class="section">
                      <h2>Plant List</h2>
                      <div id="plantList" class="plant-list">
                          ${state.plants
                            .map(
                              (plant) => `
                              <div class="plant-card">
                                  <h3>${plant.name}</h3>
                                  <p>Species: ${plant.species}</p>
                                  <p>Care Level: ${plant.careLevel}</p>
                                  <p>Water Schedule: ${plant.waterSchedule}</p>
                                  <button onclick="removePlant(${plant.id})">Remove Plant</button>
                              </div>
                          `
                            )
                            .join("")}
                      </div>
                  </div>
              </div>
          `;
  }

  window.addPlant = function () {
    const nameInput = document.getElementById("name");
    const speciesInput = document.getElementById("species");
    const careLevelInput = document.getElementById("careLevel");
    const waterScheduleInput = document.getElementById("waterSchedule");

    const newPlant = {
      id: state.plants.length + 1,
      name: nameInput.value,
      species: speciesInput.value,
      careLevel: careLevelInput.value,
      waterSchedule: waterScheduleInput.value,
    };
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_plant/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
      if (xhr.status === 200) {
        console.log("data trasfered");
        // Request was successful, you can handle the response here if needed
        render();
      } else {
        // Request failed, handle the error
        console.error("Failed to add plant:", xhr.status, xhr.statusText);
      }
    };

    // Convert the JavaScript object to a JSON string and send it in the request body
    xhr.send(JSON.stringify(newPlant));
    // xhr.send(JSON.stringify(plants));
    state.plants.push(newPlant);
    state.newPlant = {
      name: "",
      species: "",
      careLevel: "",
      waterSchedule: "",
    };
    render();
  };

  window.removePlant = function (id) {
    const index = state.plants.findIndex((plant) => plant.id === id);
    if (index !== -1) {
      state.plants.splice(index, 1);
      render();
    }
  };

  render();
});
