document.addEventListener('DOMContentLoaded', function() {
    const clearButton = document.querySelector('.btn-clear');

    if (clearButton) {
        clearButton.addEventListener('click', function(event) {
            const confirmClear = confirm('這個操作將清除所有資料，且不可恢復。你確定嗎？');
            if (!confirmClear) {
                event.preventDefault();
            }
        });
    }
});
