namespace Lab2
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnLoadGrammar = new System.Windows.Forms.Button();
            this.btnSolve = new System.Windows.Forms.Button();
            this.tbOutputGrammar = new System.Windows.Forms.TextBox();
            this.lblOutputGrammar = new System.Windows.Forms.Label();
            this.tbInputGrammar = new System.Windows.Forms.TextBox();
            this.lblInputGrammar = new System.Windows.Forms.Label();
            this.ofgOpenGrammar = new System.Windows.Forms.OpenFileDialog();
            this.SuspendLayout();
            // 
            // btnLoadGrammar
            // 
            this.btnLoadGrammar.Location = new System.Drawing.Point(118, 12);
            this.btnLoadGrammar.Name = "btnLoadGrammar";
            this.btnLoadGrammar.Size = new System.Drawing.Size(42, 23);
            this.btnLoadGrammar.TabIndex = 47;
            this.btnLoadGrammar.Text = "Load";
            this.btnLoadGrammar.UseVisualStyleBackColor = true;
            this.btnLoadGrammar.Click += new System.EventHandler(this.btnLoadGrammar_Click);
            // 
            // btnSolve
            // 
            this.btnSolve.Font = new System.Drawing.Font("Meiryo UI", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.btnSolve.Location = new System.Drawing.Point(9, 195);
            this.btnSolve.Name = "btnSolve";
            this.btnSolve.Size = new System.Drawing.Size(241, 39);
            this.btnSolve.TabIndex = 45;
            this.btnSolve.Text = "Convert grammar";
            this.btnSolve.UseVisualStyleBackColor = true;
            this.btnSolve.Click += new System.EventHandler(this.btnSolve_Click);
            // 
            // tbOutputGrammar
            // 
            this.tbOutputGrammar.Font = new System.Drawing.Font("Arial", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.tbOutputGrammar.Location = new System.Drawing.Point(268, 36);
            this.tbOutputGrammar.Multiline = true;
            this.tbOutputGrammar.Name = "tbOutputGrammar";
            this.tbOutputGrammar.ReadOnly = true;
            this.tbOutputGrammar.Size = new System.Drawing.Size(238, 153);
            this.tbOutputGrammar.TabIndex = 40;
            // 
            // lblOutputGrammar
            // 
            this.lblOutputGrammar.AutoSize = true;
            this.lblOutputGrammar.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lblOutputGrammar.Location = new System.Drawing.Point(265, 15);
            this.lblOutputGrammar.Name = "lblOutputGrammar";
            this.lblOutputGrammar.Size = new System.Drawing.Size(116, 18);
            this.lblOutputGrammar.TabIndex = 39;
            this.lblOutputGrammar.Text = "Output grammar";
            // 
            // tbInputGrammar
            // 
            this.tbInputGrammar.Font = new System.Drawing.Font("Arial", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.tbInputGrammar.Location = new System.Drawing.Point(9, 36);
            this.tbInputGrammar.Multiline = true;
            this.tbInputGrammar.Name = "tbInputGrammar";
            this.tbInputGrammar.Size = new System.Drawing.Size(241, 153);
            this.tbInputGrammar.TabIndex = 38;
            this.tbInputGrammar.Text = "a, b;\r\nS;\r\nS → a∙S∙b∙S|b∙S∙a∙S|λ;\r\nS";
            // 
            // lblInputGrammar
            // 
            this.lblInputGrammar.AutoSize = true;
            this.lblInputGrammar.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lblInputGrammar.Location = new System.Drawing.Point(9, 13);
            this.lblInputGrammar.Name = "lblInputGrammar";
            this.lblInputGrammar.Size = new System.Drawing.Size(103, 18);
            this.lblInputGrammar.TabIndex = 37;
            this.lblInputGrammar.Text = "Input grammar";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(536, 247);
            this.Controls.Add(this.btnLoadGrammar);
            this.Controls.Add(this.btnSolve);
            this.Controls.Add(this.tbOutputGrammar);
            this.Controls.Add(this.lblOutputGrammar);
            this.Controls.Add(this.tbInputGrammar);
            this.Controls.Add(this.lblInputGrammar);
            this.Name = "MainForm";
            this.Text = "Lab 2. Grammar conversion";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnLoadGrammar;
        private System.Windows.Forms.Button btnSolve;
        private System.Windows.Forms.TextBox tbOutputGrammar;
        private System.Windows.Forms.Label lblOutputGrammar;
        private System.Windows.Forms.TextBox tbInputGrammar;
        private System.Windows.Forms.Label lblInputGrammar;
        private System.Windows.Forms.OpenFileDialog ofgOpenGrammar;
    }
}

