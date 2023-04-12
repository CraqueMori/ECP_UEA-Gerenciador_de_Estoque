function exportarPDF() {
    const doc = new jsPDF();
    const carrinho = document.getElementById('carrinho').innerHTML;
    const pagamento = document.getElementById('pagamento').innerHTML;
    doc.text(carrinho, 10, 10);
    doc.text(pagamento, 10, 50);
    doc.save('carrinho.pdf');
}