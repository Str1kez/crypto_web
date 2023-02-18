const web3 = window.Web3;
const signin_url = "http://localhost:8001/api/v1/auth/signin"
const code_url = "http://localhost:8001/api/v1/auth/code"

async function get_code(formData) {
  return fetch(code_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: formData.get("username") }),
  })
    .then(response => response.json())
    .then(json => {
      if (json.code != undefined) {
        return json.code
      }
      throw new Error(JSON.stringify(json))
    })
}

function performPassword(password, codeHash) {
  const passwordHash = web3.utils.sha3(password);
  const combinedHash = web3.utils.sha3(passwordHash + codeHash);
  return combinedHash
}

async function signin(formData, code, success_field) {
  const request = await fetch(signin_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: formData.get("username"), password_hash: performPassword(formData.get("password"), code) }),
  })
  if (request.ok && request.status == 202) {
    success_field.hidden = false;
    success_field.innerHTML = `Hello, ${formData.get("username")}! <br /> You are logged in!`
    return
  }
  const json = await request.json();
  throw new Error(JSON.stringify(json));
}

function errorHandler(error, err, success) {
  data = JSON.parse(error.message);
  err.hidden = false;
  success.hidden = true;
  if (data.message != undefined) {
    err.innerHTML = data.message;
    return
  }
  let errors = "";
  console.log(data);
  for (let x of data['detail']) {
    errors += x.loc.pop() + ": " + x.msg + " <br />";
  }
  err.innerHTML = errors;
}

const form = document.forms.signin;
form.addEventListener(
  "submit",
  (event) => {
    const error_output = document.querySelector("#error");
    const success_output = document.querySelector("#success");
    const formData = new FormData(form);

    get_code(formData)
      .finally(() => { error_output.hidden = true; })
      .then(code => signin(formData, code, success_output))
      .catch(error => errorHandler(error, error_output, success_output));

    event.preventDefault();
  },
  false
);


