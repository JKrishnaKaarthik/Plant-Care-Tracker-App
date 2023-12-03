document.addEventListener("DOMContentLoaded", function () {
  const appElement = document.getElementById("app");
  const state = {
    newPlant: {
      id: "",
      name: "",
      species: "",
      careLevel: "",
      waterSchedule: "",
    },
    plants: [],
  };
  function fetchPlantList() {
    print("entered the fecthplant list function");
    fetch("/get_plant_list/")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.redirect) {
          // Redirect to the specified URL
          window.location.href = data.redirect;
        } else {
          // Do something with the received plant list
          state.plants = data.plants || [];
          console.log(data);
          render();
          // Update the state or perform other actions with the received plant list
        }
      })
      .catch((error) => {
        console.error("Error fetching plant list:", error);
      });
  }
  // Call the function to fetch plant list
  fetchPlantList();

  function render() {
    console.log("page is rendering");
    appElement.innerHTML = `
                  <div class="section">
                      <h2>Add a New Plant</h2>
                      <form id="plantForm" class="form" >
                          <label for="name">Name:</label>
                          <input type="text" name="name" value="${
                            state.newPlant.name
                          }" required>
                          <label for="species">Species:</label>
                          <input type="text" name="species" value="${
                            state.newPlant.species
                          }" required>
                          <label for="careLevel">Care Level:</label>
                          <input type="text" name="careLevel" value="${
                            state.newPlant.careLevel
                          }" required>
                          <label for="waterSchedule">Water Schedule:</label>
                          <input type="text" name="waterSchedule" value="${
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
    console.log("A plant is added");
    const nameInput = document.querySelector('input[name="name"]');
    const speciesInput = document.querySelector('input[name="species"]');
    const careLevelInput = document.querySelector('input[name="careLevel"]');
    const waterScheduleInput = document.querySelector(
      'input[name="waterSchedule"]'
    );

    const newPlant = {
      id: state.plants[state.plants.length - 1].id + 1,
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
    console.log("page is being remove", id);
    const index = state.plants.findIndex((plant) => plant.id === id);
    if (index !== -1) {
      state.plants.splice(index, 1);
      render();
    }
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove_plant/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
      if (xhr.status === 200) {
        if (xhr.responseText) {
          const responseData = JSON.parse(xhr.responseText);
          console.log("data transferred", responseData);
          // Request was successful, you can handle the response here if needed
          render();
        } else {
          console.error("Empty response received");
        }
      } else {
        // Request failed, handle the error
        console.error("Failed to remove plant:", xhr.status, xhr.statusText);
      }
    };
    // Convert the JavaScript object to a JSON string and send it in the request body
    xhr.send(JSON.stringify({ id: id }));
  };
  render();
});
