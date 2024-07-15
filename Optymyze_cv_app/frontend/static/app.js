document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    document.getElementById('spinner').style.display = 'block';

    const formData = new FormData();
    formData.append('job_description', document.getElementById('job_description').value);
    const files = document.getElementById('files').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    // Estimate time based on number of files
    const estimatedTime = Math.ceil(files.length * 0.35); // 0.35 minutes per CV
    document.getElementById('estimated-time').textContent = `Estimated time: ${estimatedTime} minutes`;

    try {
        const response = await fetch('/evaluate', {
            method: 'POST',
            body: formData
        });

        document.getElementById('spinner').style.display = 'none';

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        } else {
            displayResults(result);
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('results').textContent = 'Error in processing CVs. Please try again.';
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
