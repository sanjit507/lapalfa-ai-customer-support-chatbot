const API_URL = window.location.protocol.startsWith("http") ? "/chat" : "http://127.0.0.1:8000/chat";

// Unique Chat ID for ChatSorter memory retention
let chatId = localStorage.getItem("lapalfa_chat_id");
if (!chatId) {
    chatId = "user_" + Math.random().toString(36).substring(2, 11);
    localStorage.setItem("lapalfa_chat_id", chatId);
}

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");


// =========================================================
// ADD USER MESSAGE
// =========================================================

function addUserMessage(message) {

    const row = document.createElement("div");

    row.className = "message-row user";

    row.innerHTML = `
        <div class="message user-message">
            ${escapeHtml(message)}
        </div>
    `;

    chatBox.appendChild(row);

    scrollToBottom();
}


// =========================================================
// ADD NORMAL BOT MESSAGE
// =========================================================

function addBotMessage(message) {

    const row = document.createElement("div");

    row.className = "message-row bot";

    const formattedMessage = formatMessage(message);

    row.innerHTML = `
        <div class="message-avatar">
            L
        </div>

        <div class="message bot-message">
            ${formattedMessage}
        </div>
    `;

    chatBox.appendChild(row);

    scrollToBottom();
}

// =========================================================
// HUMAN HANDOVER CARD
// =========================================================

function addHandoverCard(message, whatsappLink) {

    const row = document.createElement("div");
    row.className = "message-row bot";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "L";

    const card = document.createElement("div");
    card.className = "handover-card";

    const text = document.createElement("div");
    text.className = "handover-text";
    text.innerHTML = formatMessage(message);
    card.appendChild(text);

    if (whatsappLink) {
        const btn = document.createElement("a");
        btn.href = whatsappLink;
        btn.target = "_blank";
        btn.rel = "noopener noreferrer";
        btn.className = "whatsapp-btn";
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15
                         -.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075
                         -.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059
                         -.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52
                         .149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52
                         -.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51
                         -.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372
                         -.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074
                         .149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625
                         .712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413
                         .248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004
                         a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648
                         -.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884
                         2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994
                         c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297
                         A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892
                         c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654
                         a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893
                         a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
            Chat on WhatsApp
        `;
        card.appendChild(btn);
    }

    row.appendChild(avatar);
    row.appendChild(card);
    chatBox.appendChild(row);
    scrollToBottom();
}



function addProductResults(answer, products) {

    const row = document.createElement("div");

    row.className = "message-row bot";


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent = "L";


    const productContainer = document.createElement("div");

    productContainer.className = "product-response";


    // Heading

    const heading = document.createElement("div");

    heading.className = "product-heading";

    heading.textContent =
        answer || "I found these products for you:";


    productContainer.appendChild(heading);


    // Product cards

    products.forEach(product => {

        const card = createProductCard(product);

        productContainer.appendChild(card);

    });


    row.appendChild(avatar);

    row.appendChild(productContainer);

    chatBox.appendChild(row);

    scrollToBottom();
}


// =========================================================
// PRODUCT CARD
// =========================================================

function createProductCard(product) {

    const card = document.createElement("div");

    card.className = "product-card";


    // -----------------------------------------------------
    // IMAGE
    // -----------------------------------------------------

    if (product.imageUrl) {

        const image = document.createElement("img");

        image.className = "product-image";

        image.src = product.imageUrl;

        image.alt =
            product.title || "Lapalfa Product";


        image.onerror = function () {

            this.style.display = "none";

        };


        card.appendChild(image);
    }


    // -----------------------------------------------------
    // CONTENT
    // -----------------------------------------------------

    const content = document.createElement("div");

    content.className = "product-content";


    // -----------------------------------------------------
    // TITLE
    // -----------------------------------------------------

    const title = document.createElement("h3");

    title.className = "product-title";

    title.textContent =
        product.title || "Product";


    content.appendChild(title);


    // -----------------------------------------------------
    // PRICE
    // -----------------------------------------------------

    const priceRow = document.createElement("div");
    priceRow.className = "product-price-row";

    const price = document.createElement("div");
    price.className = "product-price";

    if (
        product.price !== null &&
        product.price !== undefined &&
        product.price !== ""
    ) {
        price.textContent =
            `₹${Number(product.price).toLocaleString("en-IN")}`;
    } else {
        price.textContent = "Price unavailable";
    }

    priceRow.appendChild(price);

    if (
        product.comparePrice &&
        product.comparePrice > product.price
    ) {
        const compareEl = document.createElement("div");
        compareEl.className = "product-compare-price";
        compareEl.textContent =
            `₹${Number(product.comparePrice).toLocaleString("en-IN")}`;
        priceRow.appendChild(compareEl);

        const discount = Math.round(
            (1 - product.price / product.comparePrice) * 100
        );
        const badge = document.createElement("div");
        badge.className = "product-discount";
        badge.textContent = `${discount}% off`;
        priceRow.appendChild(badge);
    }

    content.appendChild(priceRow);


    // -----------------------------------------------------
    // STOCK
    // -----------------------------------------------------

    const stock = document.createElement("div");

    stock.className =
        product.inStock
            ? "product-stock in-stock"
            : "product-stock out-stock";


    stock.textContent =
        product.inStock
            ? "✓ In Stock"
            : "✕ Currently unavailable";


    content.appendChild(stock);


    // -----------------------------------------------------
    // SKU
    // -----------------------------------------------------

    if (product.sku) {

        const sku = document.createElement("div");

        sku.className = "product-sku";

        sku.textContent =
            `SKU: ${product.sku}`;

        content.appendChild(sku);
    }


    // -----------------------------------------------------
    // VIEW PRODUCT BUTTON
    // -----------------------------------------------------

    if (product.productUrl) {

        const button = document.createElement("a");

        button.className = "product-button";

        button.href =
            product.productUrl;

        button.target = "_blank";

        button.rel =
            "noopener noreferrer";

        button.textContent =
            "View Product";


        content.appendChild(button);
    }


    card.appendChild(content);


    return card;
}


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {
        return;
    }


    // Add user message

    addUserMessage(message);


    // Clear input

    messageInput.value = "";

    sendButton.disabled = true;


    // -----------------------------------------------------
    // LOADING
    // -----------------------------------------------------

    const loadingRow =
        document.createElement("div");

    loadingRow.className =
        "message-row bot";


    loadingRow.innerHTML = `
        <div class="message-avatar">
            L
        </div>

        <div class="typing-bubble">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    chatBox.appendChild(loadingRow);

    scrollToBottom();


    try {

        // -------------------------------------------------
        // API REQUEST
        // -------------------------------------------------

        const response =
            await fetch(API_URL, {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    message: message,
                    chat_id: chatId
                })

            });


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Chatbot response:",
            data
        );


        // Remove loading

        loadingRow.remove();


        // =================================================
        // PRODUCT RESPONSE
        // =================================================

        if (
            data.type === "product" &&
            Array.isArray(data.products) &&
            data.products.length > 0
        ) {

            addProductResults(
                data.answer,
                data.products
            );

        }


        // =================================================
        // HUMAN HANDOVER RESPONSE
        // =================================================

        else if (data.type === "handover") {

            addHandoverCard(
                data.answer,
                data.whatsappLink
            );

        }


        // =================================================
        // NORMAL TEXT RESPONSE
        // =================================================

        else {

            addBotMessage(
                data.answer ||
                "How can I help you?"
            );

        }


    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        loadingRow.remove();


        addBotMessage(
            "Sorry, I couldn't connect to the support server."
        );

    }


    sendButton.disabled = false;

    messageInput.focus();
}


// =========================================================
// QUICK MESSAGE
// =========================================================

function quickMessage(message) {

    messageInput.value =
        message;

    sendMessage();
}


// =========================================================
// ENTER KEY
// =========================================================

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// =========================================================
// SEND BUTTON
// =========================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// =========================================================
// SCROLL
// =========================================================

function scrollToBottom() {

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// =========================================================
// FORMAT NORMAL TEXT
// =========================================================

function formatMessage(message) {

    if (!message) {
        return "";
    }


    let text =
        escapeHtml(message);


    // New lines

    text = text.replace(
        /\n/g,
        "<br>"
    );


    // Bold markdown

    text = text.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    return text;
}


// =========================================================
// HTML ESCAPE
// =========================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}