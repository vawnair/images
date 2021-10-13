from flask import Flask, request, jsonify, render_template, send_file, redirect
import os, random, string, json, uuid
uploads = json.load(open("uploads.json", 'r'))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
exts = [".gif", ".png", ".jpeg", ".jpg", ".webm", ".mkv", ".avi", ".wmv", ".mov", ".mp4"]
emojis = ['😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '🥰', '😗', '😙', '😚', '☺️', '🙂', '🤗', '🤩', '🤔', '🤨', '😐', '😑', '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯', '😪', '😫', '😴', '😌', '😛', '😜', '😝', '🤤', '😒', '😓', '😔', '😕', '🙃', '🤑', '😲', '☹️', '🙁', '😖', '😞', '😟', '😤', '😢', '😭', '😦', '😧', '😨', '😩', '🤯', '😬', '😰', '😱', '🥵', '🥶', '😳', '🤪', '😵', '😡', '😠', '🤬', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😇', '🤠', '🥳', '🥴', '🥺', '🤥', '🤫', '🤭', '🧐', '🤓', '😈', '👿', '🤡', '👹', '👺', '💀', '☠️', '👻', '👽', '👾', '🤖', '💩', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '🙈', '🙉', '🙊', '👶', '👶🏻', '👶🏼', '👶🏽', '👶🏾', '👶🏿', '🧒', '🧒🏻', '🧒🏼', '🧒🏽', '🧒🏾', '🧒🏿', '👦', '👦🏻', '👦🏼', '👦🏽', '👦🏾', '👦🏿', '👧', '👧🏻', '👧🏼', '👧🏽', '👧🏾', '👧🏿', '🧑', '🧑🏻', '🧑🏼', '🧑🏽', '🧑🏾', '🧑🏿', '👨', '👨🏻', '👨🏼', '👨🏽', '👨🏾', '👨🏿', '👩', '👩🏻', '👩🏼', '👩🏽', '👩🏾', '👩🏿', '🧓', '🧓🏻', '🧓🏼', '🧓🏽', '🧓🏾', '🧓🏿', '👴', '👴🏻', '👴🏼', '👴🏽', '👴🏾', '👴🏿', '👵', '👵🏻', '👵🏼', '👵🏽', '👵🏾', '👵🏿', '🤵', '🤵🏻', '🤵🏼', '🤵🏽', '🤵🏾', '🤵🏿', '👰', '👰🏻', '👰🏼', '👰🏽', '👰🏾', '👰🏿', '🤰', '🤰🏻', '🤰🏼', '🤰🏽', '🤰🏾', '🤰🏿', '🤱', '🤱🏻', '🤱🏼', '🤱🏽', '🤱🏾', '🤱🏿', '👼', '👼🏻', '👼🏼', '👼🏽', '👼🏾', '👼🏿', '🎅', '🎅🏻', '🎅🏼', '🎅🏽', '🎅🏾', '🎅🏿', '🤶', '🤶🏻', '🤶🏼', '🤶🏽', '🤶🏾', '🤶🏿', '🦸', '🦸🏻', '🦸🏼', '🦸🏽', '🦸🏾', '🦸🏿', '🤳', '🤳🏻', '🤳🏼', '🤳🏽', '🤳🏾', '🤳🏿', '💪', '💪🏻', '💪🏼', '💪🏽', '💪🏾', '💪🏿', '🦵', '🦵🏻', '🦵🏼', '🦵🏽', '🦵🏾', '🦵🏿', '🦶', '🦶🏻', '🦶🏼', '🦶🏽', '🦶🏾', '🦶🏿', '👈', '👈🏻', '👈🏼', '👈🏽', '👈🏾', '👈🏿', '👉', '👉🏻', '👉🏼', '👉🏽', '👉🏾', '👉🏿', '☝️', '☝🏻', '☝🏼', '☝🏽', '☝🏾', '☝🏿', '👆', '👆🏻', '👆🏼', '👆🏽', '👆🏾', '👆🏿', '🖕', '🖕🏻', '🖕🏼', '🖕🏽', '🖕🏾', '🖕🏿', '👇', '👇🏻', '👇🏼', '👇🏽', '👇🏾', '👇🏿', '✌️', '✌🏻', '✌🏼', '✌🏽', '✌🏾', '✌🏿', '🤞', '🤞🏻', '🤞🏼', '🤞🏽', '🤞🏾', '🤞🏿', '🖖', '🖖🏻', '🖖🏼', '🖖🏽', '🖖🏾', '🖖🏿', '🤘', '🤘🏻', '🤘🏼', '🤘🏽', '🤘🏾', '🤘🏿', '🤙', '🤙🏻', '🤙🏼', '🤙🏽', '🤙🏾', '🤙🏿', '🖐️', '🖐🏻', '🖐🏼', '🖐🏽', '🖐🏾', '🖐🏿', '✋', '✋🏻', '✋🏼', '✋🏽', '✋🏾', '✋🏿', '👌', '👌🏻', '👌🏼', '👌🏽', '👌🏾', '👌🏿', '👍', '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿', '👎', '👎🏻', '👎🏼', '👎🏽', '👎🏾', '👎🏿', '✊', '✊🏻', '✊🏼', '✊🏽', '✊🏾', '✊🏿', '👊', '👊🏻', '👊🏼', '👊🏽', '👊🏾', '👊🏿', '🤛', '🤛🏻', '🤛🏼', '🤛🏽', '🤛🏾', '🤛🏿', '🤜', '🤜🏻', '🤜🏼', '🤜🏽', '🤜🏾', '🤜🏿', '🤚', '🤚🏻', '🤚🏼', '🤚🏽', '🤚🏾', '🤚🏿', '👋', '👋🏻', '👋🏼', '👋🏽', '👋🏾', '👋🏿', '🤟', '🤟🏻', '🤟🏼', '🤟🏽', '🤟🏾', '🤟🏿', '✍️', '✍🏻', '✍🏼', '✍🏽', '✍🏾', '✍🏿', '👏', '👏🏻', '👏🏼', '👏🏽', '👏🏾', '👏🏿', '👐', '👐🏻', '👐🏼', '👐🏽', '👐🏾', '👐🏿', '🙌', '🙌🏻', '🙌🏼', '🙌🏽', '🙌🏾', '🙌🏿', '🤲', '🤲🏻', '🤲🏼', '🤲🏽', '🤲🏾', '🤲🏿', '🙏', '🙏🏻', '🙏🏼', '🙏🏽', '🙏🏾', '🙏🏿', '🤝', '💅', '💅🏻', '💅🏼', '💅🏽', '💅🏾', '💅🏿', '👂', '👂🏻', '👂🏼', '👂🏽', '👂🏾', '👂🏿', '👃', '👃🏻', '👃🏼', '👃🏽', '👃🏾', '👃🏿', '🦰', '🦱', '🦲', '🦳', '👣', '👀', '👁️', '🧠', '🦴', '🦷', '👅', '👄', '💋', '💘', '❤️', '💓', '💔', '💕', '💖', '💗', '💙', '💚', '💛', '🧡', '💜', '🖤', '💝', '💞', '💟', '❣️', '💌', '💤', '💢', '💣', '💥', '💦', '💨', '💫', '💬', '🗨️', '🗯️', '💭', '🕳️', '👓', '🕶️', '🥽', '🥼', '👔', '👕', '👖', '🧣', '🧤', '🧥', '🧦', '👗', '👘', '👙', '👚', '👛', '👜', '👝', '🛍️', '🎒', '👞', '👟', '🥾', '🥿', '👠', '👡', '👢', '👑', '👒', '🎩', '🎓', '🧢', '⛑️', '📿', '💄', '💍', '💎', '🐵', '🐒', '🦍', '🐶', '🐕', '🐩', '🐺', '🦊', '🦝', '🐱', '🐈', '🦁', '🐯', '🐅', '🐆', '🐴', '🐎', '🦄', '🦓', '🦌', '🐮', '🐂', '🐃', '🐄', '🐷', '🐖', '🐗', '🐽', '🐏', '🐑', '🐐', '🐪', '🐫', '🦙', '🦒', '🐘', '🦏', '🦛', '🐭', '🐁', '🐀', '🐹', '🐰', '🐇', '🐿️', '🦔', '🦇', '🐻', '🐨', '🐼', '🦘', '🦡', '🐾', '🦃', '🐔', '🐓', '🐣', '🐤', '🐥', '🐦', '🐧', '🕊️', '🦅', '🦆', '🦢', '🦉', '🦚', '🦜', '🐸', '🐊', '🐢', '🦎', '🐍', '🐲', '🐉', '🦕', '🦖', '🐳', '🐋', '🐬', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🦀', '🦞', '🦐', '🦑', '🐌', '🦋', '🐛', '🐜', '🐝', '🐞', '🦗', '🕷️', '🕸️', '🦂', '🦟', '🦠', '💐', '🌸', '💮', '🏵️', '🌹', '🥀', '🌺', '🌻', '🌼', '🌷', '🌱', '🌲', '🌳', '🌴', '🌵', '🌾', '🌿', '☘️', '🍀', '🍁', '🍂', '🍃', '🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🥝', '🍅', '🥥', '🥑', '🍆', '🥔', '🥕', '🌽', '🌶️', '🥒', '🥬', '🥦', '🍄', '🥜', '🌰', '🍞', '🥐', '🥖', '🥨', '🥯', '🥞', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🥙', '🥚', '🍳', '🥘', '🍲', '🥣', '🥗', '🍿', '🧂', '🥫', '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🥟', '🥠', '🥡', '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥛', '☕', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻', '🥂', '🥃', '🥤', '🥢', '🍽️', '🍴', '🥄', '🔪', '🏺', '🌍', '🌎', '🌏', '🌐', '🗺️', '🗾', '🧭', '🏔️', '⛰️', '🌋', '🗻', '🏕️', '🏖️', '🏜️', '🏝️', '🏞️', '🏟️', '🏛️', '🏗️', '🧱', '🏘️', '🏚️', '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏯', '🏰', '💒', '🗼', '🗽', '⛪', '🕌', '🕍', '⛩️', '🕋', '⛲', '⛺', '🌁', '🌃', '🏙️', '🌄', '🌅', '🌆', '🌇', '🌉', '♨️', '🌌', '🎠', '🎡', '🎢', '💈', '🎪', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝', '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', '🚕', '🚖', '🚗', '🚘', '🚙', '🚚', '🚛', '🚜', '🚲', '🛴', '🛹', '🛵', '🚏', '🛣️', '🛤️', '🛢️', '⛽', '🚨', '🚥', '🚦', '🛑', '🚧', '⚓', '⛵', '🛶', '🚤', '🛳️', '⛴️', '🛥️', '🚢', '✈️', '🛩️', '🛫', '🛬', '💺', '🚁', '🚟', '🚠', '🚡', '🛰️', '🚀', '🛸', '🛎️', '🧳', '⌛', '⏳', '⌚', '⏰', '⏱️', '⏲️', '🕰️', '🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌚', '🌛', '🌜', '🌡️', '☀️', '🌝', '🌞', '⭐', '🌟', '🌠', '☁️', '⛅', '⛈️', '🌤️', '🌥️', '🌦️', '🌧️', '🌨️', '🌩️', '🌪️', '🌫️', '🌬️', '🌀', '🌈', '🌂', '☂️', '☔', '⛱️', '⚡', '❄️', '☃️', '⛄', '☄️', '🔥', '💧', '🌊', '🎃', '🎄', '🎆', '🎇', '🧨', '✨', '🎈', '🎉', '🎊', '🎋', '🎍', '🎎', '🎏', '🎐', '🎑', '🧧', '🎀', '🎁', '🎗️', '🎟️', '🎫', '🎖️', '🏆', '🏅', '🥇', '🥈', '🥉', '⚽', '⚾', '🥎', '🏀', '🏐', '🏈', '🏉', '🎾', '🥏', '🎳', '🏏', '🏑', '🏒', '🥍', '🏓', '🏸', '🥊', '🥋', '🥅', '⛳', '⛸️', '🎣', '🎽', '🎿', '🛷', '🥌', '🎯', '🎱', '🔮', '🧿', '🎮', '🕹️', '🎰', '🎲', '🧩', '🧸', '♠️', '♥️', '♦️', '♣️', '♟️', '🃏', '🀄', '🎴', '🎭', '🖼️', '🎨', '🧵', '🧶', '🔇', '🔈', '🔉', '🔊', '📢', '📣', '📯', '🔔', '🔕', '🎼', '🎵', '🎶', '🎙️', '🎚️', '🎛️', '🎤', '🎧', '📻', '🎷', '🎸', '🎹', '🎺', '🎻', '🥁', '📱', '📲', '☎️', '📞', '📟', '📠', '🔋', '🔌', '💻', '🖥️', '🖨️', '⌨️', '🖱️', '🖲️', '💽', '💾', '💿', '📀', '🧮', '🎥', '🎞️', '📽️', '🎬', '📺', '📷', '📸', '📹', '📼', '🔍', '🔎', '🕯️', '💡', '🔦', '🏮', '📔', '📕', '📖', '📗', '📘', '📙', '📚', '📓', '📒', '📃', '📜', '📄', '📰', '🗞️', '📑', '🔖', '🏷️', '💰', '💴', '💵', '💶', '💷', '💸', '💳', '🧾', '💹', '💱', '💲', '✉️', '📧', '📨', '📩', '📤', '📥', '📦', '📫', '📪', '📬', '📭', '📮', '🗳️', '✏️', '✒️', '🖋️', '🖊️', '🖌️', '🖍️', '📝', '💼', '📁', '📂', '🗂️', '📅', '📆', '🗒️', '🗓️', '📇', '📈', '📉', '📊', '📋', '📌', '📍', '📎', '🖇️', '📏', '📐', '✂️', '🗃️', '🗄️', '🗑️', '🔒', '🔓', '🔏', '🔐', '🔑', '🗝️', '🔨', '⛏️', '⚒️', '🛠️', '🗡️', '⚔️', '🔫', '🏹', '🛡️', '🔧', '🔩', '⚙️', '🗜️', '⚖️', '🔗', '⛓️', '🧰', '🧲', '⚗️', '🧪', '🧫', '🧬', '🔬', '🔭', '📡', '💉', '💊', '🚪', '🛏️', '🛋️', '🚽', '🚿', '🛁', '🧴', '🧷', '🧹', '🧺', '🧻', '🧼', '🧽', '🧯', '🛒', '🚬', '⚰️', '⚱️', '🗿', '🏧', '🚮', '🚰', '♿', '🚹', '🚺', '🚻', '🚼', '🚾', '🛂', '🛃', '🛄', '🛅', '⚠️', '🚸', '⛔', '🚫', '🚳', '🚭', '🚯', '🚱', '🚷', '📵', '🔞', '☢️', '☣️', '⬆️', '↗️', '➡️', '↘️', '⬇️', '↙️', '⬅️', '↖️', '↕️', '↔️', '↩️', '↪️', '⤴️', '⤵️', '🔃', '🔄', '🔙', '🔚', '🔛', '🔜', '🔝', '🛐', '⚛️', '🕉️', '✡️', '☸️', '☯️', '✝️', '☦️', '☪️', '☮️', '🕎', '🔯', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '⛎', '🔀', '🔁', '🔂', '▶️', '⏩', '⏭️', '⏯️', '◀️', '⏪', '⏮️', '🔼', '⏫', '🔽', '⏬', '⏸️', '⏹️', '⏺️', '⏏️', '🎦', '🔅', '🔆', '📶', '📳', '📴', '♀️', '♂️', '⚕️', '♾️', '♻️', '⚜️', '🔱', '📛', '🔰', '⭕', '✅', '☑️', '✔️', '✖️', '❌', '❎', '➕', '➖', '➗', '➰', '➿', '〽️', '✳️', '✴️', '❇️', '‼️', '⁉️', '❓', '❔', '❕', '❗', '〰️', '©️', '®️', '🔟', '💯', '🔠', '🔡', '🔢', '🔣', '🔤', '🅰️', '🆎', '🅱️', '🆑', '🆒', '🆓', 'ℹ️', '🆔', 'Ⓜ️', '🆕', '🆖', '🅾️', '🆗', '🅿️', '🆘', '🆙', '🆚', '🈁', '🈂️', '🈷️', '🈶', '🈯', '🉐', '🈹', '🈚', '🈲', '🉑', '🈸', '🈴', '🈳', '㊗️', '㊙️', '🈺', '🈵', '▪️', '▫️', '◻️', '◼️', '◽', '◾', '⬛', '⬜', '🔶', '🔷', '🔸', '🔹', '🔺', '🔻', '💠', '🔘', '🔲', '🔳', '⚪', '⚫', '🔴', '🔵', '🏁', '🚩', '🎌', '🏴', '🏳️', '🇦🇨', '🇦🇩', '🇦🇪', '🇦🇫', '🇦🇬', '🇦🇮', '🇦🇱', '🇦🇲', '🇦🇴', '🇦🇶', '🇦🇷', '🇦🇸', '🇦🇹', '🇦🇺', '🇦🇼', '🇦🇽', '🇦🇿', '🇧🇦', '🇧🇧', '🇧🇩', '🇧🇪', '🇧🇫', '🇧🇬', '🇧🇭', '🇧🇮', '🇧🇯', '🇧🇱', '🇧🇲', '🇧🇳', '🇧🇴', '🇧🇶', '🇧🇷', '🇧🇸', '🇧🇹', '🇧🇻', '🇧🇼', '🇧🇾', '🇧🇿', '🇨🇦', '🇨🇨', '🇨🇩', '🇨🇫', '🇨🇬', '🇨🇭', '🇨🇮', '🇨🇰', '🇨🇱', '🇨🇲', '🇨🇳', '🇨🇴', '🇨🇵', '🇨🇷', '🇨🇺', '🇨🇻', '🇨🇼', '🇨🇽', '🇨🇾', '🇨🇿', '🇩🇪', '🇩🇬', '🇩🇯', '🇩🇰', '🇩🇲', '🇩🇴', '🇩🇿', '🇪🇦', '🇪🇨', '🇪🇪', '🇪🇬', '🇪🇭', '🇪🇷', '🇪🇸', '🇪🇹', '🇪🇺', '🇫🇮', '🇫🇯', '🇫🇰', '🇫🇲', '🇫🇴', '🇫🇷', '🇬🇦', '🇬🇧', '🇬🇩', '🇬🇪', '🇬🇫', '🇬🇬', '🇬🇭', '🇬🇮', '🇬🇱', '🇬🇲', '🇬🇳', '🇬🇵', '🇬🇶', '🇬🇷', '🇬🇸', '🇬🇹', '🇬🇺', '🇬🇼', '🇬🇾', '🇭🇰', '🇭🇲', '🇭🇳', '🇭🇷', '🇭🇹', '🇭🇺', '🇮🇨', '🇮🇩', '🇮🇪', '🇮🇱', '🇮🇲', '🇮🇳', '🇮🇴', '🇮🇶', '🇮🇷', '🇮🇸', '🇮🇹', '🇯🇪', '🇯🇲', '🇯🇴', '🇯🇵', '🇰🇪', '🇰🇬', '🇰🇭', '🇰🇮', '🇰🇲', '🇰🇳', '🇰🇵', '🇰🇷', '🇰🇼', '🇰🇾', '🇰🇿', '🇱🇦', '🇱🇧', '🇱🇨', '🇱🇮', '🇱🇰', '🇱🇷', '🇱🇸', '🇱🇹', '🇱🇺', '🇱🇻', '🇱🇾', '🇲🇦', '🇲🇨', '🇲🇩', '🇲🇪', '🇲🇫', '🇲🇬', '🇲🇭', '🇲🇰', '🇲🇱', '🇲🇲', '🇲🇳', '🇲🇴', '🇲🇵', '🇲🇶', '🇲🇷', '🇲🇸', '🇲🇹', '🇲🇺', '🇲🇻', '🇲🇼', '🇲🇽', '🇲🇾', '🇲🇿', '🇳🇦', '🇳🇨', '🇳🇪', '🇳🇫', '🇳🇬', '🇳🇮', '🇳🇱', '🇳🇴', '🇳🇵', '🇳🇷', '🇳🇺', '🇳🇿', '🇴🇲', '🇵🇦', '🇵🇪', '🇵🇫', '🇵🇬', '🇵🇭', '🇵🇰', '🇵🇱', '🇵🇲', '🇵🇳', '🇵🇷', '🇵🇸', '🇵🇹', '🇵🇼', '🇵🇾', '🇶🇦', '🇷🇪', '🇷🇴', '🇷🇸', '🇷🇺', '🇷🇼', '🇸🇦', '🇸🇧', '🇸🇨', '🇸🇩', '🇸🇪', '🇸🇬', '🇸🇭', '🇸🇮', '🇸🇯', '🇸🇰', '🇸🇱', '🇸🇲', '🇸🇳', '🇸🇴', '🇸🇷', '🇸🇸', '🇸🇹', '🇸🇻', '🇸🇽', '🇸🇾', '🇸🇿', '🇹🇦', '🇹🇨', '🇹🇩', '🇹🇫', '🇹🇬', '🇹🇭', '🇹🇯', '🇹🇰', '🇹🇱', '🇹🇲', '🇹🇳', '🇹🇴', '🇹🇷', '🇹🇹', '🇹🇻', '🇹🇼', '🇹🇿', '🇺🇦', '🇺🇬', '🇺🇲', '🇺🇳', '🇺🇸', '🇺🇾', '🇺🇿', '🇻🇦', '🇻🇨', '🇻🇪', '🇻🇬', '🇻🇮', '🇻🇳', '🇻🇺', '🇼🇫', '🇼🇸', '🇽🇰', '🇾🇪', '🇾🇹', '🇿🇦', '🇿🇲', '🇿🇼']
dictlol = {
    ".gif":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".png":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".jpeg": ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".jpg":  ["og:image", "og:image:secure_url", "og:image:url", "summary_large_image"],
    ".webm": ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mkv":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".avi":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".wmv":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mov":  ["og:video", "twitter:player", "twitter:player:stream", "player"],
    ".mp4":  ["og:video", "twitter:player", "twitter:player:stream", "player"]
}

@app.errorhandler(400)
def error_400(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>400</h3></div>', 400

@app.errorhandler(401)
def error_401(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>401</h3></div>', 401

@app.errorhandler(403)
def error_403(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>403</h3></div>', 403

@app.errorhandler(404)
def error_404(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404

@app.errorhandler(405)
def error_405(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>405</h3></div>', 405

@app.errorhandler(429)
def error_429(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>429</h3></div>', 429

@app.errorhandler(500)
def error_500(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>500</h3></div>', 500

@app.errorhandler(502)
def error_502(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>502</h3></div>', 502

@app.errorhandler(503)
def error_503(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>503</h3></div>', 503

@app.errorhandler(504)
def error_504(error):
    return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>504</h3></div>', 504


@app.route("/")
def index():
    return redirect("https://q3h.github.io/images/")

@app.route("/cfg")
def cfg():
    return send_file("uploader.sxcu", as_attachment=True)

@app.route("/yuh.css")
def vcss():
    return """
    * {
        display: block;
        margin: auto;
    }
    body {
        background-color: #0e0e0e
    }
    """

@app.route("/gds.png")
def loll():
    return send_file("gds.png")
@app.route("/<f>")
def files(f):
    uplds = json.load(open("uploads.json", 'r'))
    if f == "favicon.ico":
        return send_file("favicon.ico")
    elif f not in uplds:
        return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404
    else:
        return render_template(uplds.get(f)[0] + ".html")

@app.route("/i/<f>")
def send_f(f):
    if os.path.exists(f"uploads/{f}") == False:
        return '<style>body{background-color: rgb(30, 30, 30);}.text{text-align: center; font-family: monospace; position: relative; top: 15%; color: rgb(255, 255, 255); text-shadow: 0px 0px 4px #ffffff;}</style><div class="text"> <h1>>.&#60;</h1> <h3>404</h3></div>', 404
    else:
        return send_file(f"uploads/{f}")

@app.route("/domains")
def domains():
    return redirect("https://raw.githubusercontent.com/q3h/images/main/domains")

@app.route("/api/upload", methods=["POST"])
def upload():
    ok = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    if os.path.exists(f"templates/{ok}.html") == True:
        ok = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    chars = "0123456789abcdef"
    color = ''.join(random.choices(chars, k=6))
    if request.args.get("type") == "file" or request.args.get("type") == None:
        uuidd = str(uuid.uuid4())
        file = request.files["file"]
        filename = file.filename
        filename = filename.lower()
        fileext = os.path.splitext(filename)[-1].lower()
        if fileext in exts:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{ok}{fileext}"))
            vars = {"{filename}": file.filename, "{size}": str(os.path.getsize(f"uploads/{ok}{fileext}")) + " Bytes", "{fileext}": fileext, "{bobux}": str(random.randint(1, 1000)) + " bobux"}
            if request.headers.get("title") == None:
                title = "host"
            elif request.headers.get("title").lower() in vars:
                title = vars.get(request.headers.get("title").lower())
            else:
                title = request.headers.get("title")
            if request.headers.get("description") == None:
                description = f"all > sxcu.net"
            elif request.headers.get("description").lower() in vars:
                description = vars.get(request.headers.get("description").lower())
            else:
                description = request.headers.get("description")
            if request.headers.get("urltype") == "invis":
                imgpath = "".join(random.choices(["​"], k=random.randint(8, 360)))
            elif request.headers.get("urltype") == "emoji":
                imgpath  = "".join(random.choices(emojis, k=random.randint(8, 64)))
            elif request.headers.get("urltype") == "noext":
                imgpath = ok
            else:
                imgpath = ok + fileext
            if request.headers.get("fakeurl") == None:
                url = "https://" + request.headers["host"] + "/" + imgpath
            else:
                url = "<" + request.headers.get("fakeurl") + ">" + "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||" + "https://" + request.headers["host"] + "/" + imgpath
            what = {
                ".gif":  ['<html xmlns="http://www.w3.org/1999/xhtml" style="height: 100%;">', '<meta name="viewport" content="width=device-width, minimum-scale=0.1">', f'<body style="margin: 0px; background: #0e0e0e; height: 100%"><img style="-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://imgs.cf/i/{ok}{fileext}" /></body></html>'],
                ".png":  ['<html xmlns="http://www.w3.org/1999/xhtml" style="height: 100%;">', '<meta name="viewport" content="width=device-width, minimum-scale=0.1">', f'<body style="margin: 0px; background: #0e0e0e; height: 100%"><img style="-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://imgs.cf/i/{ok}{fileext}" /></body></html>'],
                ".jpeg": ['<html xmlns="http://www.w3.org/1999/xhtml" style="height: 100%;">', '<meta name="viewport" content="width=device-width, minimum-scale=0.1">', f'<body style="margin: 0px; background: #0e0e0e; height: 100%"><img style="-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://imgs.cf/i/{ok}{fileext}" /></body></html>'],
                ".jpg":  ['<html xmlns="http://www.w3.org/1999/xhtml" style="height: 100%;">', '<meta name="viewport" content="width=device-width, minimum-scale=0.1">', f'<body style="margin: 0px; background: #0e0e0e; height: 100%"><img style="-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;" src="https://imgs.cf/i/{ok}{fileext}" /></body></html>'],
                ".webm": ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"],
                ".mkv":  ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"],
                ".avi":  ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"],
                ".wmv":  ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"],
                ".mov":  ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"],
                ".mp4":  ['<html xmlns="http://www.w3.org/1999/xhtml">', '<meta name="viewport" content="width=device-width">', f'<video controls="" autoplay="" name="media"><source src="https://imgs.cf/i/{ok}{fileext}" type="video/{fileext.replace(".", "")}" /></video>', "player"]
            }
            html = open(f"templates/{ok}.html", "w")
            html.write(f'{what.get(fileext)[0]}\n{what.get(fileext)[1]}\n<link rel="stylesheet" href="../yuh.css"><meta property="og:title" content="{title}">\n<meta property="twitter:title" content="{title}">\n<meta property="og:description" content="{description}">\n<meta property="twitter:description" content="{description}">' + f'<meta property="og:url" content="https://{request.headers["host"]}/{imgpath}">\n' + f'<meta name="twitter:card" content="{dictlol.get(fileext)[3]}">\n' + f'<meta property="{dictlol.get(fileext)[0]}" content="https://imgs.cf/i/{ok}{fileext}">\n' + f'<meta property="{dictlol.get(fileext)[1]}" content="https://imgs.cf/i/{ok}{fileext}">\n' + f'<meta property="{dictlol.get(fileext)[2]}" content="https://{request.headers["host"]}/i/{ok}{fileext}">\n' + f'<meta name="theme-color" content="#{color}">\n' + "\n" + what.get(fileext)[2])
            uploads[imgpath] = [ok, ok+fileext, uuidd]
            f = open("uploads.json", 'w')
            f.write(json.dumps(uploads, indent=4))
            f.close()
            return jsonify({"url": url, "file": f"https://{request.headers['host']}/i/{ok}{fileext}", "delete": f"https://{request.headers['host']}/api/delete/{imgpath}?code={uuidd}"})
        else:
            return jsonify({"error": "Invaild file extenstion (Vaild ones: .gif, .png, .jpeg, .jpg, .webm, .mkv, .avi, .wmv, .mov, .mp4)"}), 400
    elif request.args.get("type") == "paste":
        uuidd = str(uuid.uuid4())
        file = request.files["file"]
        filename = file.filename
        filename = filename.lower()
        fileext = os.path.splitext(filename)[-1].lower()
        if fileext == ".txt":
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{ok}{fileext}"))
            vars = {"{filename}": file.filename, "{size}": str(os.path.getsize(f"uploads/{ok}{fileext}")) + " Bytes", "{fileext}": fileext, "{bobux}": str(random.randint(1, 1000)) + " bobux"}
            if request.headers.get("title") == None:
                title = "host"
            elif request.headers.get("title").lower() in vars:
                title = vars.get(request.headers.get("title").lower())
            else:
                title = request.headers.get("title")
            if request.headers.get("description") == None:
                description = f"all > sxcu.net"
            elif request.headers.get("description").lower() in vars:
                description = vars.get(request.headers.get("description").lower())
            else:
                description = request.headers.get("description")
            if request.headers.get("urltype") == "invis":
                paste = "".join(random.choices(["​"], k=random.randint(8, 360)))
            elif request.headers.get("urltype") == "emoji":
                paste  = "".join(random.choices(emojis, k=random.randint(8, 64)))
            elif request.headers.get("urltype") == "noext":
                paste = ok
            else:
                paste = ok + fileext
            if request.headers.get("fakeurl") == None:
                url = "https://" + request.headers["host"] + "/" + paste
            else:
                url = "<" + request.headers.get("fakeurl") + ">" + "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||" + "https://" + request.headers["host"] + "/" + paste
            textL = open(f"uploads/{ok}{fileext}", 'r');textLL = textL.read();textL.close()
            html = open(f"templates/{ok}.html", "w")
            html.write(f'<meta property="og:title" content="{title}">\n<meta property="twitter:title" content="{title}">\n<meta property="og:description" content="{description}">\n<meta property="twitter:description" content="{description}">' + f'<meta property="og:url" content="https://{request.headers["host"]}/{paste}">\n' + f'<meta name="twitter:card" content="summary_large_image">\n' + f'<meta property="og:image" content="https://imgs.cf/gds.png">\n' + f'<meta name="theme-color" content="#{color}">\n' + f'<pre style="word-wrap: break-word; white-space: pre-wrap;">\n{textLL}\n</pre>')
            uploads[paste] = [ok, ok+fileext, uuidd]
            f = open("uploads.json", 'w')
            f.write(json.dumps(uploads, indent=4))
            f.close()
            return jsonify({"url": url, "file": f"https://{request.headers['host']}/i/{ok}{fileext}", "delete": f"https://{request.headers['host']}/api/delete/{paste}?code={uuidd}"})
        else:
            return jsonify({"error": "Not a txt file"}), 400
    else:
        return jsonify({"error": "Choose something (?type=file or ?type=paste)"}), 400

@app.route("/api/delete/<f>", methods=["GET", "POST", "DELETE"])
def rmupload(f):
    uplds = json.load(open("uploads.json", 'r'))
    if request.args.get("code") == None:
        return jsonify({"error": "Enter a key ?code=KEY"}), 400
    elif f not in uplds:
        return jsonify({"error": "File not found"}), 404
    else:
        code = request.args.get("code")
        listt = uplds.get(f)
        if code == listt[2]:
            os.remove(f"templates/{listt[0]}.html");os.remove(f"uploads/{listt[1]}");del uplds[f];j = open("uploads.json", 'w');j.write(json.dumps(uplds, indent=4));j.close();return jsonify({"msg": "File deleted!"})
        else:
            return jsonify({"msg": "Invalid key"}), 401
if __name__ == "__main__":
    ip = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 1337))
    print(f"""                                                                                
                                                               
                     //////////////////////%%%%%%%%%%%%%%%%%%                   
                ////////////////////////////////#%%%%%%%%%%%%%%%%%              
            ////////////////////////////////////////%%%%%%%%%%%%%%%%&           
          ////////////////////////////////////////////(%%%%%%%%%%%%%%%%         
        /////////////////////////////////////////////////%%%%%%%%%%%%%%%&       
      ////////////////////////////////////////////////////######%%%%%%%%%%      
     ///////////////(((############%///////////////////////########%%%%%%%%     
    ////////////(#######################%#//////////////////##########%%%%%%    
    /////////(##############################%////////////////##########%%%%%%   
   #//////(#######(((((((((((((#####%&         (/////////////###########%%%%%   
   %////(####((((((((((((((((((#                 (///////////###########%%%%%   
    ///###((((((((((((((((((#                      //////////############%%%%   
    (/##(((((((((((((((((#                          (///////############%%%%%   
     #(((((((((((((((((#//#                          //////############%%%%%%   
    #((((((((((((((((((////                          %////#############%%%%%    
    ((((((((((((((((#(//////                          (/#############%%%%%%(    
   %(((((((((((((((((////////                         ############%%%%%%%%(/(   
   %(((((((((((((((#//////////                      %########%%%%%%%%%%%%////   
   %((((((((((((((((////////////                %%%%%%%%%%%%%%%%%%%%%%%#/////   
    ((((((((((((((((//////////////        %%%%%%%%%%%%%%%%%%%%%%%%%%%#///////   
    (((((((((((((((#//////////////*/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%//////////   
     #((((((((((((((//////////////*****/&%%%%%%%%%%%%%%%%%%%%%%(////////////    
      #(((((((((((((#//////////////*********//%%%%%%%%%%%(//**//////////////    
       ##((((((((((((((/////////////*************************/////////////&     
        %###(((((((((((#//////////////*********************//////////////       
          ######(((((((((%///////////////***************///////////////         
            &###############%//////////////////***//////////////////            
                #################///////////////////////////////&               
                    #################%/////////////////////                     

                                Worst image host.
                                https://github.com/q3h/images  
    """)
    app.run(host=ip, port=port, threaded=True)
