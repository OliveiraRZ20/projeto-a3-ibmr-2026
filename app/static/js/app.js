document.querySelectorAll('input[name="cpf"], input[name="cpf_destino"]').forEach((input) => {
  input.addEventListener('input', () => {
    const digits = input.value.replace(/\D/g, '').slice(0, 11);
    input.value = digits.length > 9
      ? `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9)}`
      : digits;
  });
});
