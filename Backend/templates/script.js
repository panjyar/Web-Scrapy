document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch and display news items from a specified API endpoint
    function fetchNews(apiEndpoint, listElementId) {
        fetch(apiEndpoint)
            .then(response => response.json())
            .then(data => {
                const newsList = document.getElementById(listElementId);
                newsList.innerHTML = ''; // Clear the list before adding new items

                data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item.latestNews || item.latestNewstitlenits || item.noticeTitle || item.eventName || item.tenderTitle;
                    newsList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching news:', error));
    }

    // Fetch news from all three sources
    fetchNews('/api/citnews', 'cit-news-list');
    fetchNews('/api/iitgnews', 'iitg-news-list');
    fetchNews('/api/nitsnews', 'nits-news-list');
});
