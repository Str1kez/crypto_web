const backend_url = "http://localhost:8001/api/v1/auth/signup"

const form = document.forms.signup;
form.addEventListener(
  "submit",
  (event) => {
    const error_output = document.querySelector("#error");
    const success_output = document.querySelector("#success");
    const formData = new FormData(form);

    fetch(backend_url, {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (response.status != 201) {
          return response.json();
        }
        error_output.hidden = true;
        success_output.hidden = false;
      })
      .then(result => {
        if (result.message != undefined) {
          error_output.innerHTML = result.message;
        } else {
          let errors = "";
          for (let x of result['detail']) {
            errors += x.loc.pop() + ": " + x.msg + " <br />";
          }
          error_output.innerHTML = errors;
        }
        error_output.hidden = false;
        success_output.hidden = true;
      });

    event.preventDefault();
  },
  false
);

