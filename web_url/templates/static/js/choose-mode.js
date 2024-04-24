document.addEventListener('DOMContentLoaded', function() {
  const toggle1 = document.getElementById('switch1');
  const toggle2 = document.getElementById('switch2');
  const toggle3 = document.getElementById('switch3');
  const card1 = document.getElementById('item1');
  const card2 = document.getElementById('item2');
  const card3 = document.getElementById('item3');
  const mode1 = document.getElementById('chart_1');
  const mode2 = document.getElementById('chart_2');
  const mode3 = document.getElementById('chart_3');

  // 初始化时设置 item1 为选中状态，并显示 card1
  toggle1.checked = true;
  card1.style.display = 'block';
  card2.style.display = 'none';
  card3.style.display = 'none';
  mode1.style.display = 'block';
  mode2.style.display = 'none';
  mode3.style.display = 'none';

  toggle1.addEventListener('change', function() {
    if (toggle1.checked) {
      card1.style.display = 'block';
      card2.style.display = 'none';
      card3.style.display = 'none';
      mode1.style.display = 'block';
      mode2.style.display = 'none';
      mode3.style.display = 'none';
      toggle2.checked = false;
      toggle3.checked = false;
    } else {
      toggle2.checked = false;
      toggle3.checked = false;
    }
  });

  toggle2.addEventListener('change', function() {
    if (toggle2.checked) {
      card2.style.display = 'block';
      card1.style.display = 'none';
      card3.style.display = 'none';
      mode1.style.display = 'none';
      mode2.style.display = 'block';
      mode3.style.display = 'none';
      toggle1.checked = false;
      toggle3.checked = false;
    } else {
      toggle1.checked = false;
      toggle3.checked = false;
    }
  });

  toggle3.addEventListener('change', function() {
    if (toggle3.checked) {
      card3.style.display = 'block';
      card1.style.display = 'none';
      card2.style.display = 'none';
      mode1.style.display = 'none';
      mode2.style.display = 'none';
      mode3.style.display = 'block';
      toggle1.checked = false;
      toggle2.checked = false;
    } else {
      toggle1.checked = false;
      toggle2.checked = false;
    }
  });
});
