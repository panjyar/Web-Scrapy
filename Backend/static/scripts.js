document.addEventListener('DOMContentLoaded', function () {
    fetchAllNews();
});

function fetchAllNews() {
    fetch('/api/news')
        .then(response => response.json())
        .then(data => {
            categorizeNews(data);
        })
        .catch(error => console.error('Error fetching news:', error));
}

function categorizeNews(data) {
    const citNewsTableBody = document.getElementById('citNewsTable').querySelector('tbody');
    const noticesTableBody = document.getElementById('noticesTable').querySelector('tbody');
    const tendersTableBody = document.getElementById('tendersTable').querySelector('tbody');
    const latestNewsTableBody = document.getElementById('latestNewsTable').querySelector('tbody');

    // Populate CIT News Title Section
    data.citNews.forEach(item => {
        // Display main news
        if (item.news) {
            const newsRow = document.createElement('tr');
            newsRow.innerHTML = `<td>${item.news}</td><td><a href="${item.newslink}" target="_blank">Link</a></td>`;
            citNewsTableBody.appendChild(newsRow);
        }

        // CIT Notice Table
        if (item.noticeTitle) {
            const noticeRow = document.createElement('tr');
            noticeRow.innerHTML = `<td>${item.noticeTitle}</td><td><a href="${item.noticeUrl}" target="_blank">Link</a></td>`;
            noticesTableBody.appendChild(noticeRow);
        }

        // Display Tenders
        if (item.tenderTitle) {
            const tenderRow = document.createElement('tr');
            tenderRow.innerHTML = `<td>${item.tenderTitle}</td><td><a href="${item.tenderUrl}" target="_blank">Link</a></td>`;
            tendersTableBody.appendChild(tenderRow);
        }

        // Display Latest News
        if (item.eventName) {
            const latestNewsRow = document.createElement('tr');
            latestNewsRow.innerHTML = `<td>${item.eventName}</td> <td>${item.eventDate}</td> <td><a href="${item.eventInfo}" target="_blank">Link</a></td>`;
            latestNewsTableBody.appendChild(latestNewsRow);
        }

        // Display Latest News from NITs
        if (item.latestNewstitlenits) {
            const latestNitsRow = document.createElement('tr');
            latestNitsRow.innerHTML = `<td>${item.latestNewstitlenits}</td><td><a href="${item.latestNewsurlnits}" target="_blank">Link</a></td>`;
            latestNewsTableBody.appendChild(latestNitsRow);
        }
    });
}