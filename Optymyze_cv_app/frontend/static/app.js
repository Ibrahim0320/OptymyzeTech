document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    document.getElementById('spinner').style.display = 'block';

    const formData = new FormData();
    formData.append('job_description', document.getElementById('job_description').value);
    const files = document.getElementById('files').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

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
    const formattedResults = result.result.map(item => `${item[0]}: ${item[1]}`).join('<br>');
    resultsDiv.innerHTML = `
        <h2>Results:</h2>
        <div class="content-container"><pre>${formattedResults}</pre></div>
        <h2>Optymyze AI Assessment of Top 10% of Candidates</h2>
        <div class="content-container">${result.chatgpt_report}</div>
        <a href="/download/${result.zip_name}" class="button">Download Top CVs</a>
    `;
}
