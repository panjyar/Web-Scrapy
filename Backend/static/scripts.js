document.addEventListener('DOMContentLoaded', function () {
    fetchAllNews();
    fetchNotice();
    // Uncomment and define the following if needed
    // fetchNews();
    // fetchUpcommingNews();
    fetchTender();
});

function fetchAllNews() {
    fetch('/api/all') 
        .then(response => response.json())
        .then(data => {
            displayNews(data);
        })
        .catch(error => console.error('Error fetching NITS news:', error));
}

function displayNews(data) {
    const NewsTable = document.getElementById('news1').querySelector('tbody');
    NewsTable.innerHTML = ''; 
    data.News.forEach(item => {
        if (item.news) {
            const newsRow = document.createElement('tr');
            newsRow.innerHTML = `<td>${item.news}</td><td><a href="${item.newslink}" target="_blank">Link</a></td>`;
            NewsTable.appendChild(newsRow);
        }
    });
}

function fetchNotice() {
    fetch('/api/all') 
        .then(response => response.json())
        .then(data => {
            displayNotice(data);
            displayUpcommingEvent(data);
        })
        .catch(error => console.error('Error fetching NITS news:', error));
}

function displayNotice(data) {
    const NoticeTable = document.getElementById('notices').querySelector('tbody');
    NoticeTable.innerHTML = ''; 
    data.Notices.forEach(item => {
        if (item.noticeTitle) {
            const noticeRow = document.createElement('tr');
            noticeRow.innerHTML = `<td>${item.noticeTitle}</td><td><a href="${item.noticeUrl}" target="_blank">Link</a></td>`;
            NoticeTable.appendChild(noticeRow);
        }
    });
}
function displayUpcommingEvent(data) {
    const UpcommingEventTable = document.getElementById('upcommingEvent').querySelector('tbody');
    UpcommingEventTable.innerHTML = ''; 
    data.UpcomingEvents.forEach(item => {
        if (item.eventName) {
            const UpcomingEventRow = document.createElement('tr');
            UpcomingEventRow.innerHTML = `<td>${item.eventName}</td><td>${item.eventDate}</td><td><a href="${item.eventInfo}" target="_blank">Link</a></td>`;
            UpcommingEventTable.appendChild(UpcomingEventRow);
        }
    });
}
    function fetchTender() {
        fetch('/api/all') 
            .then(response => response.json())
            .then(data => {
                displayTender(data);
                
            })
            .catch(error => console.error('Error fetching Tender:', error));
    }
    
    function displayTender(data) {
        const TenderTable = document.getElementById('tenders').querySelector('tbody');
        TenderTable.innerHTML = ''; 
        data.Tenders.forEach(item => {
            if (item.tenderTitle) {
                const TenderRow = document.createElement('tr');
                TenderRow.innerHTML = `<td>${item.tenderTitle}</td><td><a href="${item.tenderUrl}" target="_blank">Link</a></td>`;
                TenderTable.appendChild(TenderRow);
            }
        });
    }

