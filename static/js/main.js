document.getElementById('boothForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Clear previous results and steps
    document.getElementById('binaryResult').textContent = '';
    document.getElementById('steps').innerHTML = '';
    document.getElementById('steps').classList.add('hidden');

    // Get new inputs
    const m = document.getElementById('m').value;
    const r = document.getElementById('r').value;

    // Fetch result from the backend
    const response = await fetch('/booth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ m, r })
    });

    const data = await response.json();

    // Display the binary result
    document.getElementById('binaryResult').textContent = `Binary Result: ${data.result}`;
    document.getElementById('result').classList.remove('hidden');

    // Add event listener to "Show Steps" button
    document.getElementById('showSteps').addEventListener('click', () => {
        const stepsDiv = document.getElementById('steps');
        stepsDiv.innerHTML = data.steps.map(step => `<p class="p-3 bg-gray-700 rounded-lg">${step}</p>`).join('');
        stepsDiv.classList.remove('hidden'); // Show steps div
    });
});