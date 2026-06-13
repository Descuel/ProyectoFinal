function login() {
    const codigo = document.getElementById("username").value; // 👈 aquí debe ser codigo
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            codigo: codigo,   // 👈 backend espera "codigo"
            password: password
        })
    })
    .then(res => res.json().then(data => {
        return {
            status: res.status,
            data: data
        }
    }))
    .then(resultado => {
        if (resultado.status === 200) {
            localStorage.setItem("token", resultado.data.token);
            window.location.href = "/dashboard";
        } else {
            alert(resultado.data.mensaje); // 👈 muestra error si credenciales incorrectas
        }
    })
    .catch(error => {
        console.error(error);
    });
}
