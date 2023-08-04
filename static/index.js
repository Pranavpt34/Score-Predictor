// JavaScript to show each letter one by one and the full word
const textContainer = document.getElementById('text-container');
const letters = textContainer.getElementsByTagName('span');
const totalLetters = letters.length;
let currentIndex = 0;

function showNextLetter() {
  letters[currentIndex].classList.remove('hidden');
  currentIndex = (currentIndex + 1) % totalLetters;
  if (currentIndex === 0) {
    setTimeout(hideAllLetters, 1000);
  } else {
    setTimeout(showNextLetter, 1000);
  }
}

function hideAllLetters() {
  for (let i = 0; i < totalLetters; i++) {
    letters[i].classList.add('hidden');
  }
  setTimeout(showNextLetter, 1000);
}

showNextLetter(); // Start the sequence


// Fetch teams when the page loads

function fetchTeams() {
  fetch('/get_teams')
    .then(response => response.json())
    .then(data => {
      const teamDropdown = document.getElementById('team-dropdown');
      data.teams.forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.textContent = team;
        teamDropdown.appendChild(option);
      });
    })
    .catch(error => console.error('Error fetching teams:', error));
}



//fetch players
function fetchPlayers() {
  const selectedTeam = document.getElementById('team-dropdown').value;
  if (selectedTeam) {
    fetch('/get_players', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'selected_team': selectedTeam })
    })
      .then(response => response.json())
      .then(data => {
        const checkboxContainer = document.getElementById("checkboxContainer");
        checkboxContainer.innerHTML = ''; // Clear previous checkboxes

        data.players.forEach(player => {
          const checkboxDiv = createCheckbox(player);
          checkboxContainer.appendChild(checkboxDiv);
        });
      })
      .catch(error => console.error('Error fetching players:', error));
  }
}

// Function to create checkboxes
function createCheckbox(name) {
  const checkboxDiv = document.createElement("div");
  checkboxDiv.className = "form-check";

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "form-check-input";
  checkbox.name = "players"; // Change the name to 'players' for multiple checkboxes
  checkbox.value = name;

  const label = document.createElement("label");
  label.className = "form-check-label";
  label.textContent = name;

  checkboxDiv.appendChild(checkbox);
  checkboxDiv.appendChild(label);

  return checkboxDiv;
}

// fetch opposition
function fetchOpposition() {
  const selectedTeam = document.getElementById('team-dropdown').value;
  console.log("Clear12")
  fetch('/get_opposition', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'selected_team': selectedTeam })
  })
    .then(response => response.json())
    .then(response => {
      console.log("responses from bCK", response); // Log the response to check the data
      const oppositionDropdown = document.getElementById('opposition-dropdown');
      oppositionDropdown.innerHTML = '';

      response.opposition.forEach(opposition => {
        const option = document.createElement('option');
        option.value = opposition;
        option.textContent = opposition;
        oppositionDropdown.appendChild(option);
      });

      oppositionDropdown.disabled = false;
      document.getElementById('submit-button').disabled = false;
    })
    .catch(error => console.error('Error fetching teams:', error));
}




// fetch demo
function fetchGrounds() {
  fetch('/get_grounds')
    .then(response => response.json())
    .then(data => {
      const groundDropdown = document.getElementById('ground-dropdown');
      groundDropdown.innerHTML = ''; // Clear previous options
      data.grounds.forEach(ground => {
        const option = document.createElement('option');
        option.value = ground;
        option.textContent = ground;
        groundDropdown.appendChild(option);
      });
      groundDropdown.disabled = false; // Enable ground dropdown
      document.getElementById('submit-button').disabled = false; // Enable submit button
    })
    .catch(error => console.error('Error fetching teams:', error));
}
function enableSubmitButton() {
  document.getElementById('submit-button').disabled = false;
}



function submitSelection() {
  const selectedPlayers = Array.from(document.querySelectorAll('input[name="players"]:checked')).map(checkbox => checkbox.value);
  const selectedTeam = document.getElementById('team-dropdown').value;
  const selectedGround = document.getElementById('ground-dropdown').value;
  const selectedOpposite = document.getElementById('opposition-dropdown').value;
  document.getElementById("submit-button").disabled = true;

  const requestData = {
    'selected_team': selectedTeam,
    'selected_player': selectedPlayers,
    'selected_ground': selectedGround,
    'selected_opposition': selectedOpposite
  };

  // window.location = window.location.href;
  fetch('/submit_selection', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      const table = document.querySelector('.table')
      console.log(table)

      function generateTable(data) {

        const table = document.getElementById("playerTable").getElementsByTagName('tbody')[0];



        for (const player in data) {
          if (data.hasOwnProperty(player)) {
            const row = table.insertRow();
            const playerCell = row.insertCell();
            const scoreCell = row.insertCell();
            const ballCell = row.insertCell();

            playerCell.innerHTML = player;
            scoreCell.innerHTML = data[player][0]; // Display the first element of the array (Run)
            ballCell.innerHTML = data[player][1];  // Display the second element of the array (Ball)
          }
        }


      }



      generateTable(data)

      const formElement = document.getElementById('team-dropdown');
      formElement.selectedIndex = 0;

      const checkboxContainer = document.getElementById('checkboxContainer');
      checkboxContainer.innerHTML = ""

    })
    .catch(error => console.error('Error submitting selection:', error));
}

fetchTeams();
fetchGrounds();