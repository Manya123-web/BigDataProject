const searchInput = document.getElementById('searchInput');
const resultsGrid = document.getElementById('resultsGrid');
const loading = document.getElementById('loading');
const noResults = document.getElementById('noResults');
const statsBar = document.getElementById('statsBar');
const resultCount = document.getElementById('resultCount');

// Debounce
let timeout = null;

searchInput.addEventListener('input', (e) => {
    clearTimeout(timeout);
    if(e.target.value.length > 2) {
        timeout = setTimeout(() => performSearch(e.target.value), 500);
    } else if (e.target.value.length === 0) {
        resultsGrid.innerHTML = '';
        noResults.classList.add('hidden');
        statsBar.classList.add('hidden');
    }
});

async function performSearch(query) {
    loading.classList.remove('hidden');
    resultsGrid.innerHTML = '';
    noResults.classList.add('hidden');
    statsBar.classList.add('hidden');

    try {
        const response = await fetch(`/recommend?query=${encodeURIComponent(query)}&k=9`);
        const data = await response.json();

        loading.classList.add('hidden');

        if (data.recommendations && data.recommendations.length > 0) {
            renderResults(data.recommendations);
            resultCount.innerText = data.recommendations.length;
            statsBar.classList.remove('hidden');
        } else {
            noResults.classList.remove('hidden');
        }

    } catch (error) {
        console.error('Error:', error);
        loading.classList.add('hidden');
    }
}

function renderResults(facultyList) {
    resultsGrid.innerHTML = facultyList.map((faculty, index) => {
        // Fallback image handling
        const imageUrl = faculty.image_url || 'https://via.placeholder.com/300x200?text=NO+IMAGE'; // Use placeholder if null

        const citations = faculty.citations || 0;
        const works = faculty.works_count || 0;
        const topics = faculty.topics || "General Research";
        
        return `
            <div class="faculty-card" style="animation: fadeInUp 0.5s ease backwards ${index * 0.1}s">
                <div class="card-image-container">
                    <img src="${imageUrl}" alt="${faculty.name}" onerror="this.src='https://via.placeholder.com/300x200?text=OFFLINE'">
                </div>
                <div class="card-content">
                    <h2 class="faculty-name">${faculty.name}</h2>
                    <span class="faculty-role">${faculty.faculty_type}</span>
                    
                    <div class="stat-row">
                        <span>MATCH ACCURACY</span>
                        <span>${Math.round(faculty.similarity_score * 100)}%</span>
                    </div>
                    <div class="stat-row">
                        <span>CITATIONS</span>
                        <span>${citations}</span>
                    </div>
                     <div class="stat-row">
                        <span>WORKS</span>
                        <span>${works}</span>
                    </div>

                    <div class="topics">
                        TOPICS: ${topics}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}
