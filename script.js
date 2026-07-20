// ===== ESTADO DA APLICAÇÃO =====
// Carrega tarefas salvas no localStorage, ou começa com array vazio
let tarefas = JSON.parse(localStorage.getItem('tarefas')) || [];
let filtroAtual = 'todas';

// ===== ELEMENTOS DO DOM =====
const form = document.getElementById('form-tarefa');
const input = document.getElementById('input-tarefa');
const lista = document.getElementById('lista-tarefas');
const contador = document.getElementById('contador');
const botoesFiltro = document.querySelectorAll('.filtro');

// ===== FUNÇÕES =====

function salvarTarefas() {
  localStorage.setItem('tarefas', JSON.stringify(tarefas));
}

function adicionarTarefa(texto) {
  const novaTarefa = {
    id: Date.now(), // id único simples baseado no timestamp
    texto: texto,
    concluida: false
  };
  tarefas.push(novaTarefa);
  salvarTarefas();
  renderizar();
}

function alternarConclusao(id) {
  tarefas = tarefas.map(tarefa =>
    tarefa.id === id ? { ...tarefa, concluida: !tarefa.concluida } : tarefa
  );
  salvarTarefas();
  renderizar();
}

function removerTarefa(id) {
  tarefas = tarefas.filter(tarefa => tarefa.id !== id);
  salvarTarefas();
  renderizar();
}

function obterTarefasFiltradas() {
  if (filtroAtual === 'pendentes') {
    return tarefas.filter(t => !t.concluida);
  }
  if (filtroAtual === 'concluidas') {
    return tarefas.filter(t => t.concluida);
  }
  return tarefas; // 'todas'
}

function renderizar() {
  const tarefasFiltradas = obterTarefasFiltradas();

  // Limpa a lista atual
  lista.innerHTML = '';

  // Recria cada item na tela
  tarefasFiltradas.forEach(tarefa => {
    const li = document.createElement('li');
    if (tarefa.concluida) li.classList.add('concluida');

    li.innerHTML = `
      <input type="checkbox" ${tarefa.concluida ? 'checked' : ''}>
      <span>${tarefa.texto}</span>
      <button>Excluir</button>
    `;

    // Checkbox: marcar/desmarcar como concluída
    li.querySelector('input').addEventListener('change', () => {
      alternarConclusao(tarefa.id);
    });

    // Botão: remover tarefa
    li.querySelector('button').addEventListener('click', () => {
      removerTarefa(tarefa.id);
    });

    lista.appendChild(li);
  });

  // Atualiza contador
  const pendentes = tarefas.filter(t => !t.concluida).length;
  contador.textContent = `${pendentes} tarefa(s) pendente(s) de ${tarefas.length} no total`;
}

// ===== EVENTOS =====

form.addEventListener('submit', (evento) => {
  evento.preventDefault(); // impede o reload da página
  const texto = input.value.trim();
  if (texto === '') return; // ignora entradas vazias

  adicionarTarefa(texto);
  input.value = '';
  input.focus();
});

botoesFiltro.forEach(botao => {
  botao.addEventListener('click', () => {
    // Atualiza qual botão está "ativo" visualmente
    botoesFiltro.forEach(b => b.classList.remove('ativo'));
    botao.classList.add('ativo');

    filtroAtual = botao.dataset.filtro;
    renderizar();
  });
});

// ===== INICIALIZAÇÃO =====
renderizar();