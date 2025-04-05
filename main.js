// Main JavaScript for College Rankings Video Generator

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const pipelineForm = document.getElementById('pipeline-form');
    const loadingSpinner = document.getElementById('loading-spinner');
    const videosContainer = document.getElementById('videos-container');
    const noVideosMessage = document.getElementById('no-videos-message');
    
    const dataCollectionStatus = document.getElementById('data-collection-status');
    const videoGenerationStatus = document.getElementById('video-generation-status');
    const lastRun = document.getElementById('last-run');

    // Update status badges with animation
    function updateStatusBadge(element, status) {
        const oldStatus = element.textContent.toLowerCase();
        const newStatus = status.replace('_', ' ');
        
        if (oldStatus !== newStatus) {
            element.classList.add('status-change');
            setTimeout(() => {
                element.classList.remove('status-change');
            }, 500);
        }
        
        element.textContent = status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ');
        element.className = 'badge status-badge';
        
        if (status === 'not_started') {
            element.classList.add('bg-secondary');
        } else if (status === 'in_progress') {
            element.classList.add('bg-warning');
        } else if (status === 'completed') {
            element.classList.add('bg-success');
        } else if (status === 'failed') {
            element.classList.add('bg-danger');
        }
    }

    // Fetch initial status
    function fetchStatus() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                updateStatusBadge(dataCollectionStatus, data.data_collection);
                updateStatusBadge(videoGenerationStatus, data.video_generation);
                
                if (data.last_run) {
                    lastRun.textContent = data.last_run;
                }
                
                if (data.videos_generated && data.videos_generated.length > 0) {
                    displayVideos(data.videos_generated);
                }
            })
            .catch(error => {
                console.error('Error fetching status:', error);
            });
    }

    // Display generated videos with animation
    function displayVideos(videos) {
        if (videos.length === 0) {
            noVideosMessage.style.display = 'block';
            return;
        }
        
        noVideosMessage.style.display = 'none';
        videosContainer.innerHTML = '';
        
        videos.forEach((video, index) => {
            const videoElement = document.createElement('div');
            videoElement.className = 'video-container';
            videoElement.style.opacity = '0';
            videoElement.style.transform = 'translateY(20px)';
            videoElement.innerHTML = `
                <div class="video-preview">
                    <div>
                        <h5>${video.category}</h5>
                        <p>Audio: ${video.audio_mood}</p>
                    </div>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6>${video.category}</h6>
                        <small class="text-muted">Generated: ${video.timestamp}</small>
                    </div>
                    <div>
                        <a href="${video.url}" class="btn btn-sm btn-outline-primary" target="_blank">View Details</a>
                        <button class="btn btn-sm btn-outline-success download-btn" data-url="${video.url}">Download</button>
                    </div>
                </div>
            `;
            videosContainer.appendChild(videoElement);
            
            // Animate entry with delay based on index
            setTimeout(() => {
                videoElement.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                videoElement.style.opacity = '1';
                videoElement.style.transform = 'translateY(0)';
            }, 100 * index);
        });
        
        // Add event listeners to download buttons
        document.querySelectorAll('.download-btn').forEach(button => {
            button.addEventListener('click', function() {
                const url = this.getAttribute('data-url');
                // In a real implementation, this would trigger a download
                // For this demo, we'll just open the URL in a new tab
                window.open(url, '_blank');
            });
        });
    }

    // Poll for status updates every 3 seconds when pipeline is running
    let statusInterval = null;
    
    function startStatusPolling() {
        if (statusInterval) {
            clearInterval(statusInterval);
        }
        statusInterval = setInterval(fetchStatus, 3000);
    }
    
    function stopStatusPolling() {
        if (statusInterval) {
            clearInterval(statusInterval);
            statusInterval = null;
        }
    }

    // Handle form submission with validation
    pipelineForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get selected categories
        const checkboxes = document.querySelectorAll('.category-checkbox:checked');
        const selectedCategories = Array.from(checkboxes).map(cb => cb.value);
        
        if (selectedCategories.length === 0) {
            showAlert('Please select at least one ranking category.', 'danger');
            return;
        }
        
        // Get selected audio mood
        const audioMood = document.getElementById('audio-mood').value;
        
        // Show loading spinner
        loadingSpinner.style.display = 'block';
        
        // Disable form
        const formElements = pipelineForm.elements;
        for (let i = 0; i < formElements.length; i++) {
            formElements[i].disabled = true;
        }
        
        // Start polling for status updates
        startStatusPolling();
        
        // Run pipeline
        fetch('/api/run_pipeline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                categories: selectedCategories,
                audio_mood: audioMood
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Enable form
            for (let i = 0; i < formElements.length; i++) {
                formElements[i].disabled = false;
            }
            
            // Show success message
            showAlert(`Successfully generated ${data.videos.length} videos!`, 'success');
            
            // Stop polling after a short delay to ensure we get the final status
            setTimeout(() => {
                stopStatusPolling();
                fetchStatus(); // One final status check
            }, 3000);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.style.display = 'none';
            
            // Enable form
            for (let i = 0; i < formElements.length; i++) {
                formElements[i].disabled = false;
            }
            
            // Show error message
            showAlert('An error occurred while generating videos. Please try again.', 'danger');
            
            // Stop polling
            stopStatusPolling();
        });
    });

    // Show alert message
    function showAlert(message, type) {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
        alertContainer.role = 'alert';
        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insert at the top of the form
        pipelineForm.parentNode.insertBefore(alertContainer, pipelineForm);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertContainer.classList.remove('show');
            setTimeout(() => {
                alertContainer.remove();
            }, 500);
        }, 5000);
    }

    // Select/Deselect all categories in a section
    document.querySelectorAll('.select-all-btn').forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            const checkboxes = document.querySelectorAll(`.category-checkbox[data-section="${sectionId}"]`);
            const selectAll = this.getAttribute('data-select') === 'true';
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = selectAll;
            });
            
            // Toggle button text and data attribute
            if (selectAll) {
                this.textContent = 'Deselect All';
                this.setAttribute('data-select', 'false');
            } else {
                this.textContent = 'Select All';
                this.setAttribute('data-select', 'true');
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Fetch initial status on page load
    fetchStatus();
});
