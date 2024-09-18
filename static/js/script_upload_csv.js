document.getElementById('upload-form').onsubmit = function(event) {
    event.preventDefault();  // 防止表單自動提交

    const formData = new FormData(this);
    fetch(uploadCsvUrl, {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'conflict') {
                const conflictingRows = data.conflicting_rows;
                const newEntries = data.new_entries;
                showConflictDialog(conflictingRows, newEntries);  // 顯示模態框
            } else if (data.status === 'success') {
                window.location.href = showDataUrl;  // 直接跳轉到 show_data 頁面
            }
        })
        .catch(error => console.error('Error:', error));
};

function showConflictDialog(conflictingRows, newEntries) {
    const modal = document.getElementById('alert-dialog');
    modal.style.display = 'block';

    document.getElementById('overwrite-btn').onclick = function() {
        resolveConflicts('overwrite', conflictingRows);
        modal.style.display = 'none';
    };

    document.getElementById('skip-btn').onclick = function() {
        resolveConflicts('skip', [], newEntries);
        modal.style.display = 'none';
    };

    document.getElementById('cancel-btn').onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}

function resolveConflicts(action, conflictingRows = [], newEntries = []) {
    fetch(resolveConflictsUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            action: action,
            conflicting_rows: conflictingRows,
            new_entries: newEntries
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = showDataUrl;
            }
        })
        .catch(error => console.error('Error:', error));
}
