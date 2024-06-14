document.getElementById('cvForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('job_description', document.getElementById('jobDescription').value);
    const files = document.getElementById('cvFiles').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
        const response = await fetch('/evaluate', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results:</h2>';
    const ul = document.createElement('ul');

    for (const [cv, score] of Object.entries(result)) {
        const li = document.createElement('li');
        li.textContent = `${cv}: ${score}`;
        ul.appendChild(li);
    }

    resultsDiv.appendChild(ul);
}
