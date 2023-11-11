// 시/도(select id = sido) 요소와 시/군구(select id = sigg) 요소 가져오기
const sidoSelect = document.getElementById('sido');
const siggSelect = document.getElementById('sigg');


// 시/도 선택 상자가 변경될 때 실행할 함수를 정의
sidoSelect.addEventListener('change', function () {
    const selectedSido = sidoSelect.value;

    // 시/도를 선택하지 않은 경우 시/군구 선택 상자를 비활성화하고 초기화
    if (!selectedSido) {
        siggSelect.innerHTML = '<option value="" disabled selected>상세지역</option>';
        siggSelect.disabled = true;
        
    } else {
        // 시/도를 선택한 경우, AJAX 요청으로 서버에서 해당 시/도에 속하는 시/군구 목록을 가져오기
        fetch(`/get_sigg_list/?sido=${selectedSido}`)
            .then(response => response.json())
            .then(data => {
                siggSelect.innerHTML = '<option value="" disabled selected>상세지역</option>';
    
                // 서버에서 받은 데이터로 시/군구 선택 상자를 업데이트
                data.forEach(sigg => {
                    siggSelect.innerHTML += `<option value="${sigg.name}">${sigg.name}</option>`;
                });

                // 시/군구 선택 상자를 활성화
                siggSelect.disabled = false;

                // default값 설정
                // siggSelect.selectedIndex = 1;
                selected_sigg.value = siggSelect.options[1].value;
            });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    siggSelect.innerHTML = '<option value="" disabled selected>상세지역</option>';
    siggSelect.disabled = true;
});