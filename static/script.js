// Genel site JS dosyası
// Buraya site genelinde kullanılacak küçük yardımcı fonksiyonlar konabilir.

// Örnek: basit bir DOM ready helper
function ready(fn){
  if(document.readyState!='loading') return fn();
  document.addEventListener('DOMContentLoaded', fn);
}

// Örnek: küçük bir flash link focus davranışı
ready(function(){
  var flash = document.querySelector('.flash');
  if(flash){
    flash.addEventListener('click', function(){ this.style.display='none'; });
  }
});
