function submitImage(imagePath) {
    // 특정 이미지가 클릭되면 해당 이미지의 정보를 form에 추가하고 form을 제출
    const form = document.getElementById('imageForm');

    // 이미지 정보를 form에 추가
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'selected_image';
    input.value = imagePath;
    form.appendChild(input);

    // form 제출
    form.submit();
}
