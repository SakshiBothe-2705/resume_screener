document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const analyzeBtn = document.getElementById('analyze-btn');
    const jobDescInput = document.getElementById('job-desc');
    const resultsContainer = document.getElementById('results-container');
    const statusText = document.getElementById('status-text');

    let selectedFiles = [];

    // Drag & Drop Handlers
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        const newFiles = Array.from(files);
        selectedFiles = [...selectedFiles, ...newFiles];
        renderFileList();
    }

    function renderFileList() {
        fileList.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <span><i class="fa-regular fa-file"></i> ${file.name}</span>
                <i class="fa-solid fa-xmark" style="cursor:pointer;" onclick="removeFile(${index})"></i>
            `;
            fileList.appendChild(item);
        });
    }

    window.removeFile = (index) => {
        selectedFiles.splice(index, 1);
        renderFileList();
    };

    // Analyze Button Handler
    analyzeBtn.addEventListener('click', async () => {
        const jobDesc = jobDescInput.value.trim();
        
        if (!jobDesc) {
            alert('Please enter a Job Description.');
            return;
        }
        if (selectedFiles.length === 0) {
            alert('Please upload at least one resume.');
            return;
        }

        // UI Loading State
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        statusText.innerText = 'Processing...';
        resultsContainer.innerHTML = '';

        const formData = new FormData();
        formData.append('job_description', jobDesc);
        selectedFiles.forEach(file => {
            formData.append('resumes', file);
        });

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                renderResults(data.results);
                statusText.innerText = `${data.results.length} Resumes Ranked`;
            } else {
                alert('Error: ' + data.error);
                statusText.innerText = 'Error occurred';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while communicating with the server.');
            statusText.innerText = 'Connection Error';
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> Analyze Resumes';
        }
    });

    function renderResults(results) {
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="empty-state">
                    <p>No matches found or text could not be extracted.</p>
                </div>
            `;
            return;
        }

        results.forEach((result, index) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            card.innerHTML = `
                <div class="result-header">
                    <span class="filename">${result.filename}</span>
                    <span class="score">${result.score}% Match</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
                <p class="preview-text">${result.preview}</p>
            `;
            
            resultsContainer.appendChild(card);

            // Animate entrance
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                card.querySelector('.progress-fill').style.width = `${result.score}%`;
            }, index * 100 + 50);
        });
    }
});
