import os
import gradio as gr
import google.generativeai as genai

# API Key-г нууцаар авах тохиргоо (Hugging Face эсвэл Local дээр ажиллана)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ai_teacher_system(topic, level, task_type):
    if not api_key:
        return "Алдаа: API Key тохируулаагүй байна!"
        
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Чи бол Монгол улсын боловсролын стандартын дагуу ажилладаг заах арга зүйч багш.
    Сэдэв: {topic}
    Түвшин: {level}
    Даалгаврын төрөл: {task_type}
    
    Дээрх мэдээлэлд үндэслэн сурагчдад зориулсан даалгавар бэлд. 
    Бүтэц:
    1. Онолын товч санамж.
    2. 3-5 бодлого эсвэл асуулт.
    3. Зөв хариултууд (тусдаа хэсэгт).
    Хариултыг Монгол хэлээр маш ойлгомжтой бичээрэй.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# Дизайн хэсэг
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🍎 AI-д суурилсан Ухаалаг Багшийн Систем")
    
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(label="Хичээлийн сэдэв", placeholder="Жишээ нь: 5-р ангийн математик")
            level = gr.Dropdown(["Суурь", "Дунд", "Гүнзгий"], label="Түвшин", value="Дунд")
            task_type = gr.Radio(["Сонгох тест", "Бодлого"], label="Төрөл", value="Сонгох тест")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        
        with gr.Column():
            output = gr.Markdown("Даалгавар энд гарна.")

    btn.click(fn=ai_teacher_system, inputs=[topic, level, task_type], outputs=output)

if __name__ == "__main__":
    app.launch()
