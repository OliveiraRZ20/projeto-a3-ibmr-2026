document.querySelectorAll('[data-cpf-input]').forEach((input) => {
  const hiddenInput = input.form.querySelector(
    `[data-cpf-value][name="${input.dataset.cpfName}"]`,
  );

  input.addEventListener('input', () => {
    const digits = input.value.replace(/\D/g, '').slice(0, 11);
    if (digits.length > 9) {
      input.value = `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9)}`;
    } else if (digits.length > 6) {
      input.value = `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6)}`;
    } else if (digits.length > 3) {
      input.value = `${digits.slice(0, 3)}.${digits.slice(3)}`;
    } else {
      input.value = digits;
    }
  });

  input.form.addEventListener('submit', () => {
    hiddenInput.value = input.value.replace(/\D/g, '').slice(0, 11);
  });
});

const phoneInput = document.querySelector('input[name="telefone"]');
if (phoneInput) {
  const formatPhone = () => {
    const digits = phoneInput.value.replace(/\D/g, '').slice(0, 11);
    if (digits.length > 7) {
      phoneInput.value = `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
    } else if (digits.length > 2) {
      phoneInput.value = `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
    } else if (digits.length === 2) {
      phoneInput.value = `(${digits})`;
    } else if (digits.length === 1) {
      phoneInput.value = `(${digits}`;
    } else {
      phoneInput.value = digits;
    }
  };

  phoneInput.addEventListener('input', () => {
    formatPhone();
  });

  phoneInput.form.addEventListener('submit', () => {
    phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 11);
  });
}

const nameInput = document.querySelector('[data-name-input]');
if (nameInput) {
  const normalizeName = () => {
    nameInput.value = nameInput.value
      .replace(/[^\p{L}\s]/gu, '')
      .replace(/\s+/g, ' ')
      .replace(/^\s+/, '')
      .split(' ')
      .map((part) => part
        ? `${part.charAt(0).toLocaleUpperCase('pt-BR')}${part.slice(1).toLocaleLowerCase('pt-BR')}`
        : '')
      .join(' ');
  };

  nameInput.addEventListener('input', () => {
    nameInput.value = nameInput.value.replace(/[^\p{L}\s]/gu, '');
  });
  nameInput.addEventListener('blur', normalizeName);
  nameInput.form.addEventListener('submit', normalizeName);
}

const emailInput = document.querySelector('input[name="email"]');
if (emailInput) {
  emailInput.addEventListener('input', () => {
    emailInput.value = emailInput.value
      .replace(/[^A-Za-z0-9._%+@-]/g, '')
      .toLowerCase();
  });
}

document.querySelectorAll('[data-password-toggle]').forEach((button) => {
  button.addEventListener('click', () => {
    const input = button.parentElement.querySelector('input');
    input.type = input.type === 'password' ? 'text' : 'password';
    button.textContent = input.type === 'password' ? 'Mostrar' : 'Ocultar';
  });
});

if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('.metric-card, .balance-highlight').forEach((card) => {
    card.addEventListener('pointermove', (event) => {
      const bounds = card.getBoundingClientRect();
      const rotateX = ((event.clientY - bounds.top) / bounds.height - 0.5) * -2;
      const rotateY = ((event.clientX - bounds.left) / bounds.width - 0.5) * 2;
      card.style.transform = `translateY(-3px) perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    card.addEventListener('pointerleave', () => {
      card.style.transform = '';
    });
  });
}

const password = document.querySelector('input[name="senha"]');
const passwordConfirmation = document.querySelector('input[name="confirmacao_senha"]');
const passwordMatch = document.querySelector('[data-password-match]');
const allowedPasswordCharacters = new Set(
  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{};:,.?',
);
document.querySelectorAll('[data-password-input]').forEach((input) => {
  input.addEventListener('input', () => {
    input.value = [...input.value]
      .filter((character) => allowedPasswordCharacters.has(character))
      .join('');
  });
});

if (password && passwordConfirmation && passwordMatch) {
  const comparePasswords = () => {
    if (!passwordConfirmation.value) {
      passwordMatch.textContent = '';
      passwordConfirmation.setCustomValidity('');
    } else if (password.value !== passwordConfirmation.value) {
      passwordMatch.textContent = 'As senhas não coincidem.';
      passwordConfirmation.setCustomValidity('As senhas não coincidem.');
    } else {
      passwordMatch.textContent = 'As senhas coincidem.';
      passwordConfirmation.setCustomValidity('');
    }
  };
  password.addEventListener('input', comparePasswords);
  passwordConfirmation.addEventListener('input', comparePasswords);
}
