using System;
using System.IO;
using System.Windows.Forms;
using CompilerConstructionLib;

namespace Lab2
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void btnSolve_Click(object sender, EventArgs e)
        {
            Grammar inputGrammar;
            try
            {
                inputGrammar = Grammar.Parse(tbInputGrammar.Text);
            }
            catch (Exception exception)
            {
                MessageBox.Show(@"Wrong input: " + exception.Message);
                return;
            }

            try
            {
                tbOutputGrammar.Text = new NonShortenGrammar(inputGrammar).ToString();
            }
            catch (Exception exception)
            {
                MessageBox.Show(@"Incorrect input grammar: " + exception.Message);
                return;
            }
        }

        private void btnLoadGrammar_Click(object sender, EventArgs e)
        {
            if (ofgOpenGrammar.ShowDialog() == DialogResult.OK)
            {
                tbInputGrammar.Text = File.ReadAllText(ofgOpenGrammar.FileName);
            }
        }
    }
}
