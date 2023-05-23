document.addEventListener("DOMContentLoaded", () => {

    let socket = io();
  
    // Configure button
    socket.on("connect", () => {
      // User join
      socket.emit("joined");
  
      // Forget user's last channel
      document.querySelector("#newChannel").addEventListener("click", () => {
        //alert("forget");
        socket.emit("exit");
        localStorage.removeItem("last_channel");
      });
  
      // When user leaves channel redirect to '/'
      document.querySelector("#leave").addEventListener("click", () => {
        // User has left
        //alert("exit");
        socket.emit("exit");
  
        localStorage.removeItem("last_channel");
        window.location.replace("/");
      });
  
  
      document.querySelector("#comment").addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
          document.getElementById("send-button").click();
        }
      });
  
      // Send button emits a "send message" event
      document.querySelector("#send-button").addEventListener("click", () => {
        let timestamp = new Date();
        timestamp = timestamp.toLocaleTimeString();
        //alert("semd");
        // Save user message
        let msg = document.getElementById("comment").value;
        socket.emit("send message", msg, timestamp);
  
        // Clear input
        document.getElementById("comment").value = "";
      });
    });
  
    // When user joins a channel
    socket.on("status", (data) => {
      // Joined user
  
      infoMessage(data.msg);
  
      // Save user current channel on localStorage
      localStorage.setItem("last_channel", data.channel);
    });
  
    socket.on("announce message", (data) => {
      // Format message
      let timestamp = data.timestamp;
      let userMessage = data.user;
      let message = data.msg;
  
      createMessage(timestamp, userMessage, message);
    });
  
    function createMessage(timestamp, user, msg) {
      let ul = document.querySelector("#chat");
      let li = document.createElement("li");
      let p = document.createElement("p");
  
      user = user.charAt(0).toUpperCase() + user.slice(1);
  
      let pUser = createElement("strong", "user", user);
      let pMsg = createElement("span", "msg", msg);
      let pTimestamp = createElement("small", "time", timestamp);
  
      let br = document.createElement("br");
  
      li.appendChild(pUser);
      li.appendChild(document.createTextNode(" "));
      li.appendChild(pTimestamp);
      li.appendChild(br);
      li.appendChild(pMsg);
  
      li.setAttribute("class", "messageBox");
  
      ul.append(li);
    }
  
    function createElement(element, cls, text) {
      let el = document.createElement(element);
      el.appendChild(document.createTextNode(text));
      el.setAttribute("class", cls);
  
      return el;
    }
  
    function infoMessage(msg) {
      let chat = document.querySelector("#chat");
      let message = createElement("p", "message-info", msg);
      chat.appendChild(message);
    }
  });
  