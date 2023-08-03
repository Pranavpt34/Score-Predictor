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
            console.log("Here it is",data)
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
          console.log("data", data.players)
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

// submit form to player list to backend
function submitPlayerSelection() {
    const selectedPlayers = Array.from(document.querySelectorAll('input[name="players"]:checked')).map(checkbox => checkbox.value);
    console.log("Here is data",selectedPlayers)
    // Replace '/submit_players' with the actual endpoint URL in your Flask app
    fetch('/submit_players', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'selected_players': selectedPlayers })
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the Flask server if needed
        console.log(data);
      })
      .catch(error => console.error('Error submitting players:', error));
  }

function fetchGrounds() {
    console.log("hello ground1")
    const selectedTeam = document.getElementById('team-dropdown').value;
    console.log(selectedTeam)
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
    .catch(error => console.error('Error fetching grounds:', error));
}

function enableSubmitButton() {
    document.getElementById('submit-button').disabled = false;
}

function submitSelection() {
    const selectedPlayers = Array.from(document.querySelectorAll('input[name="players"]:checked')).map(checkbox => checkbox.value);
    const selectedTeam = document.getElementById('team-dropdown').value;
    const selectedGround = document.getElementById('ground-dropdown').value;

    const requestData = {
        'selected_team': selectedTeam,
        'selected_player': selectedPlayers,
        'selected_ground': selectedGround
    };

    fetch('/submit_selection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json)
    .then(data => {
        console.log(data.message);
    })
    .catch(error => console.error('Error submitting selection:', error));
}

fetchTeams(); 
fetchGrounds();