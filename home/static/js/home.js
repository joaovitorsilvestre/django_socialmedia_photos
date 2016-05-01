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
          var a = document.createElement("A")
          var bnt = document.createElement("INPUT");       //cria um elemento input
          bnt.type = "SUBMIT"                             // define o tipo do input
          bnt.value = results[i]                            //adiciona o texto ao botao
          bnt.className = "item_search"

          a.href = "usuario/".concat(bnt.value)
          a.appendChild(bnt)
          display_search_box.appendChild(a);              //adiciona ao div

          num_itens += 1
      }
    }

    display_search(true, num_itens);

    //return results[0]
}
