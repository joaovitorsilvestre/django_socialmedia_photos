function login_over(on) {
    var login_button = document.getElementById("login_button")
    if (on == true){
        login_button.style.backgroundColor = "#439AAB"
    }
    else{
        login_button.style.backgroundColor = "#204A52"
    }
}

function display_search(on, num_itens) {
    var display_search_box = document.getElementById("display_search_box")
    if (on == true){
      display_search_box.style.display = "inline"
    }
    else {
      display_search_box.style.display = "none"
    }

    if (num_itens == 0) {
        display_search_box.style.display = 'none'
    }
    else{
        var tamanho = 20
        for (i=0; i<num_itens; i++) {
            tamanho += 20
            display_search_box.style.height = tamanho.toString() + 'px'
        }
    }

}

function filtrar_resultados(texto_pesquisa) {
    var display_search_box = document.getElementById('display_search_box');

    while( display_search_box.hasChildNodes()) {
        display_search_box.removeChild(display_search_box.lastChild);
    }

    var num_itens = 0

    for (i = 0; i < results.length; i++) {            // para cada item no results

      if (results[i].indexOf(texto_pesquisa) > -1) {       // verifica se o texto digitado está no item atual do for
          var bnt = document.createElement("BUTTON");       //cria um elemento button
          var b_t = document.createTextNode(results[i]);    // cria um elemento texto

          bnt.appendChild(b_t);                             //adiciona o texto ao botao
          display_search_box.appendChild(bnt);              //adiciona ao div

          num_itens += 1
      }
    }

    //agora vamos editar o css dos elementos
    var elementos = display_search_box.getElementsByTagName("BUTTON")
    for (i=0; i<elementos.length; i++) {
        elementos[i].className = "item_search"
    }


    display_search(true, num_itens);

    //return results[0]
}
