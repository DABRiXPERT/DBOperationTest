document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('data-table');
    const clearDataBtn = document.getElementById('clear-data-btn');
    const alertDialog = document.getElementById('alert-dialog');
    const confirmClearBtn = document.getElementById('confirm-clear-btn');
    const cancelClearBtn = document.getElementById('cancel-clear-btn');
    const clearForm = document.getElementById('clear-form');

    // 單列刪除功能
    table.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-delete-row')) {
            if (confirm('確定要刪除這一行資料嗎？')) {
                const row = event.target.closest('tr');
                const id = row.getAttribute('data-id');

                // 創建一個隱藏的表單提交刪除請求
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/delete_row/${id}/`;

                const csrfToken = document.createElement('input');
                csrfToken.type = 'hidden';
                csrfToken.name = 'csrfmiddlewaretoken';
                csrfToken.value = getCsrfToken();  // 獲取 CSRF Token

                form.appendChild(csrfToken);
                document.body.appendChild(form);
                form.submit();  // 提交表單刪除資料
            }
        }
    });

    // 顯示清除資料對話框
    clearDataBtn.addEventListener('click', function() {
        alertDialog.style.display = 'block';
    });

    // 確認清除所有資料
    confirmClearBtn.addEventListener('click', function() {
        clearForm.submit(); // 提交表單清除資料
    });

    // 取消清除
    cancelClearBtn.addEventListener('click', function() {
        alertDialog.style.display = 'none'; // 隱藏對話框
    });

    // 點擊模態外部時關閉對話框
    window.addEventListener('click', function(event) {
        if (event.target === alertDialog) {
            alertDialog.style.display = 'none';
        }
    });

    // 單元格編輯功能，當使用者點擊單元格時提示輸入新值
    table.addEventListener('click', function(event) {
        const cell = event.target;

        if (cell.classList.contains('editable')) {
            const id = cell.closest('tr').getAttribute('data-id');
            const field = cell.getAttribute('data-field');
            const currentValue = cell.textContent.trim();

            let newValue;
            if (field === 'unix_month') {
                newValue = prompt('請輸入新的日期 (格式：YYYYMM):', currentValue);
                if (!/^\d{4}(0[1-9]|1[0-2])$/.test(newValue)) {
                    alert('輸入的日期格式不正確，請重新輸入 (YYYYMM)');
                    return;
                }
            } else {
                newValue = prompt('請輸入新的數值:', currentValue);
                if (isNaN(newValue)) {
                    alert('輸入的必須是數值，請重新輸入');
                    return;
                }
                newValue = parseFloat(newValue).toFixed(1); // 格式化為浮點數
            }

            // 更新資料行
            fetch(`/update_row/${id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ field: field, value: newValue })
            }).then(response => {
                if (response.ok) {
                    window.location.reload(); // 成功更新後刷新頁面
                } else {
                    alert('更新失敗，請重試');
                }
            }).catch(error => {
                console.error('發送更新請求時出錯:', error);
            });
        }
    });

    // CSRF Token 獲取
    function getCsrfToken() {
        const cookieValue = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : '';
    }
});